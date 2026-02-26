/** @odoo-module **/

import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Component, onWillStart, onWillDestroy, useState } from "@odoo/owl";

export class PackageMoverAction extends Component {
    setup() {
        this.moverService = useService("package_mover");
        this.barcodeService = useService("barcode");

        this.state = useState(this.moverService.state);

        this.onBarcodeScanned = this._onBarcodeScanned.bind(this);
        
        onWillStart(() => {
            if (this.barcodeService.bus) {
                this.barcodeService.bus.addEventListener("barcode_scanned", this.onBarcodeScanned);
            }
        });

        onWillDestroy(() => {
            if (this.barcodeService.bus) {
                this.barcodeService.bus.removeEventListener("barcode_scanned", this.onBarcodeScanned);
            }
        });
    }

    _onBarcodeScanned(ev) {
        this.moverService.processScan(ev.detail.barcode);
    }

    onManualLocationKeydown(ev) {
        if (ev.key === "Enter") {
            const value = ev.target.value.trim();
            if (value) {
                this.moverService.processScan(value);
                ev.target.value = ""; 
            }
        }
    }

    selectPackage(pkg) {
        this.moverService.selectPackage(pkg);
    }

    removePackage(pkg) {
        this.moverService.removePackage(pkg.id);
    }

    triggerMove() {
        this.moverService.triggerMove();
    }

    triggerMoveAll() {
        this.moverService.triggerMoveAll();
    }

    triggerLoadFromLocation() {
        this.moverService.triggerLoadFromLocation();
    }

    clearList() {
        this.moverService.reset();
    }

    cancelMove() {
        this.moverService.cancelMove();
    }

    backToList() {
        this.moverService.backToList();
    }
}

PackageMoverAction.template = "tug_barcode_custom.MainTemplate";
registry.category("actions").add("tug_barcode_custom_client_action", PackageMoverAction);