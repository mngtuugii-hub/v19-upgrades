/** @odoo-module **/

import { registry } from "@web/core/registry";
import { reactive } from "@odoo/owl";

export const packageMoverService = {
    dependencies: ["orm", "notification"],
    
    start(env, { orm, notification }) {
        // Reactive state that persists across the session
        const state = reactive({
            mode: 'list', // 'list' or 'detail'
            scannedPackages: [], // Array of package objects
            activePackage: null, // The package currently being viewed
            waitingForLocation: false, // If true, next scan is treated as destination
            waitingForSourceLocation: false, // New: If true, next scan is treated as source location
            isBatchMove: false, // Track if we are moving one or all
        });

        async function processScan(barcode) {
            if (state.waitingForLocation) {
                await _handleLocationScan(barcode);
            } else if (state.waitingForSourceLocation) {
                await _handleSourceLocationScan(barcode);
            } else {
                await _handlePackageScan(barcode);
            }
        }

        async function _handlePackageScan(barcode) {
            try {
                // Search for package by barcode
                const packages = await orm.searchRead("stock.quant.package", [['name', '=', barcode]], ['id']);
                
                if (packages.length) {
                    const pkgId = packages[0].id;
                    
                    // Check if already in list to avoid double fetching
                    const existingIndex = state.scannedPackages.findIndex(p => p.id === pkgId);
                    if (existingIndex !== -1) {
                        selectPackage(state.scannedPackages[existingIndex]);
                        notification.add(`Package already in list.`, { type: "info" });
                        return;
                    }

                    const details = await orm.call("stock.quant.package", "get_package_contents_info", [pkgId]);
                    
                    state.scannedPackages.push(details);
                    notification.add(`Package ${details.name} added.`, { type: "success" });
                    
                    // Logic: 1st package -> Details, 2nd+ -> List
                    if (state.scannedPackages.length === 1) {
                        selectPackage(details);
                    } else {
                        state.mode = 'list';
                        state.activePackage = null;
                    }
                } else {
                    notification.add(`No package found for barcode: ${barcode}`, { type: "danger" });
                }
            } catch (e) {
                console.error(e);
                notification.add("Error scanning package.", { type: "danger" });
            }
        }

        async function _handleLocationScan(barcode) {
            try {
                // BRANCH 1: Batch Move (Move All)
                if (state.isBatchMove) {
                    const pkgIds = state.scannedPackages.map(p => p.id);
                    const result = await orm.call("stock.quant.package", "action_batch_move_to_location", [pkgIds, barcode]);
                    
                    if (result.success) {
                        notification.add(result.message, { type: "success" });
                        reset(); // Reset everything after a successful batch move
                    } else {
                        notification.add(result.message, { type: "danger" });
                    }
                    return;
                }

                // BRANCH 2: Single Move (Active Package)
                if (!state.activePackage) return;

                const result = await orm.call("stock.quant.package", "action_move_to_location", [state.activePackage.id, barcode]);
                
                if (result.success) {
                    notification.add(result.message, { type: "success" });
                    
                    state.mode = 'list';
                    state.waitingForLocation = false;
                    
                    // Remove moved package from list
                    state.scannedPackages = state.scannedPackages.filter(p => p.id !== state.activePackage.id);
                    state.activePackage = null;
                } else {
                    notification.add(result.message, { type: "danger" });
                }
            } catch (e) {
                console.error(e);
                notification.add("Error moving package(s).", { type: "danger" });
            }
        }

        async function _handleSourceLocationScan(barcode) {
            try {
                const result = await orm.call("stock.quant.package", "action_get_packages_from_location", [barcode]);
                
                if (result.success) {
                    const newPackages = result.packages;
                    let addedCount = 0;
                    
                    // Merge new packages
                    newPackages.forEach(pkg => {
                        if (!state.scannedPackages.some(p => p.id === pkg.id)) {
                            state.scannedPackages.push(pkg);
                            addedCount++;
                        }
                    });

                    notification.add(result.message, { type: "success" });
                    
                    // Stop waiting for source
                    state.waitingForSourceLocation = false;
                    state.mode = 'list';
                    state.activePackage = null;

                } else {
                    notification.add(result.message, { type: "danger" });
                }
            } catch (e) {
                console.error(e);
                notification.add("Error loading packages from location.", { type: "danger" });
            }
        }

        function selectPackage(pkg) {
            state.activePackage = pkg;
            state.mode = 'detail';
            state.waitingForLocation = false;
            state.waitingForSourceLocation = false;
            state.isBatchMove = false;
        }

        function removePackage(pkgId) {
            state.scannedPackages = state.scannedPackages.filter(p => p.id !== pkgId);
            if (state.activePackage && state.activePackage.id === pkgId) {
                state.activePackage = null;
                state.mode = 'list';
            }
        }

        function triggerMove() {
            state.waitingForLocation = true;
            state.waitingForSourceLocation = false;
            state.isBatchMove = false;
            notification.add("Scan destination Location for this package.", { type: "info" });
        }

        function triggerMoveAll() {
            if (state.scannedPackages.length === 0) return;
            state.waitingForLocation = true;
            state.waitingForSourceLocation = false;
            state.isBatchMove = true;
            notification.add(`Scan destination to move ALL ${state.scannedPackages.length} packages.`, { type: "info" });
        }

        function triggerLoadFromLocation() {
            state.waitingForSourceLocation = true;
            state.waitingForLocation = false;
            state.isBatchMove = false;
            notification.add("Scan Source Location to load packages.", { type: "info" });
        }

        function cancelMove() {
            state.waitingForLocation = false;
            state.waitingForSourceLocation = false;
            state.isBatchMove = false;
        }

        function backToList() {
            state.mode = 'list';
            state.activePackage = null;
            state.waitingForLocation = false;
            state.waitingForSourceLocation = false;
            state.isBatchMove = false;
        }

        function reset() {
            state.scannedPackages = [];
            state.activePackage = null;
            state.mode = 'list';
            state.waitingForLocation = false;
            state.waitingForSourceLocation = false;
            state.isBatchMove = false;
        }

        return {
            state,
            processScan,
            selectPackage,
            removePackage,
            triggerMove,
            triggerMoveAll,
            triggerLoadFromLocation, // Exported new method
            cancelMove,
            backToList,
            reset
        };
    }
};

registry.category("services").add("package_mover", packageMoverService);