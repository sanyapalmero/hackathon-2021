import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { ProductsRoutingModule } from './products-routing.module';
import { ProductsComponent } from './products.component';
import { TuiButtonModule, TuiLinkModule, TuiLoaderModule, TuiTableModeModule } from "@taiga-ui/core";
import { TuiInputModule, TuiTagModule } from "@taiga-ui/kit";
import { TuiTableModule, TuiTablePaginationModule } from "@taiga-ui/addon-table";
import { TuiLetModule } from "@taiga-ui/cdk";
import { FormsModule, ReactiveFormsModule } from "@angular/forms";
import { ProductComponent } from './product/product.component';
import { TableModule } from "primeng/table";


@NgModule({
  declarations: [
    ProductsComponent,
    ProductComponent
  ],
    imports: [
        CommonModule,
        ProductsRoutingModule,
        TuiTableModeModule,
        TuiButtonModule,
        TuiTagModule,
        TuiLinkModule,
        TuiTableModule,
        TuiLetModule,
        TuiLoaderModule,
        TuiInputModule,
        TuiTablePaginationModule,
        FormsModule,
        ReactiveFormsModule,
        TableModule
    ]
})
export class ProductsModule { }
