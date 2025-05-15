/** @odoo-module **/
import { DropdownItem } from "@web/core/dropdown/dropdown_item";
import { Component } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog"
import { ConfirmationDialog } from "@web/core/confirmation_dialog/confirmation_dialog";

import { _t } from "@web/core/l10n/translation";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { STATIC_ACTIONS_GROUP_NUMBER } from "@web/search/action_menus/action_menus";
// /media/data1/project1/d1337/odoo-docker/addons/storage/fs_file/static/src/views/fields
import { FSFileField } from "@fs_file/views/fields/fsfile_field.esm";

const cl = console.log

const cogMenuRegistry = registry.category("cogMenu");
const dialogRegistry = registry.category("dialog");

/**
 * 'Import records' menu
 *
 * This component is used to import the records for particular model.
 * @extends Component
 */
export class ImportRecordModal extends Component {
	static template = "base_om.ImportRecordModal"
	static components = { 
		Dialog, 
		FSFileField
	};

	setup() {
		super.setup();
	}
}

export class ImportRecordsx extends Component {
	static template = "base_om.ImportRecordsx";
	static components = { DropdownItem };

	setup() {
		super.setup();

		this.action = useService("action");
		this.rpc = useService("rpc");
		this.orm = useService('orm')
		this.notification = useService("notification");
		this.dialogService = useService("dialog");

		// const resPartner = await this.orm.call('res.partner','search_read',[[]])
	}

	//---------------------------------------------------------------------
	// Protected
	//---------------------------------------------------------------------

	importRecords() {
		const { context, resModel } = this.env.searchModel;
		this.action.doAction({
			type: "ir.actions.client",
			tag: "import",
			params: { model: resModel, context },
		});
	}

	async testx() {
		console.log("testx", 1)
		console.log(registry.getAll())

		// wip do custom import / show wizard form
		// wip keep / del
	}
}

ImportRecordsx.template = "base_om.ImportRecordsx"

export const importRecordsItem = {
	Component: ImportRecordsx,
	// groupNumber: STATIC_ACTIONS_GROUP_NUMBER,
};

cl("dialogRegistry", dialogRegistry)
cogMenuRegistry.add("import-menu-m1", importRecordsItem, { sequence: 1 });
dialogRegistry.add("import-menu-modal", {
	Component: ImportRecordModal
}, { sequence: 1 });
