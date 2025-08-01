import { analyticModels } from "@analytic/../tests/analytic_test_helpers";
import { mailModels } from "@mail/../tests/mail_test_helpers";
import { ProjectTask } from "@project/../tests/mock_server/mock_models/project_task";
import { SaleOrderLine } from "@sale/../tests/mock_server/mock_models/sale_order_line";
import { defineModels } from "@web/../tests/web_test_helpers";

export const saleTimesheetModels = {
    ProjectTask,
    SaleOrderLine,
};

export function defineSaleTimesheetModels() {
    return defineModels({ ...mailModels, ...analyticModels, ...saleTimesheetModels });
}
