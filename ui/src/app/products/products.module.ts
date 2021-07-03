import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { ProductsRoutingModule } from './products-routing.module';
import { ProductsComponent } from './products.component';
import { TuiButtonModule, TuiLinkModule, TuiLoaderModule, TuiTableModeModule } from "@taiga-ui/core";
import { TuiTagModule } from "@taiga-ui/kit";
import { TuiTableModule } from "@taiga-ui/addon-table";
import { TuiLetModule } from "@taiga-ui/cdk";


@NgModule({
  declarations: [
    ProductsComponent
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
    TuiLoaderModule
  ]
})
export class ProductsModule { }
