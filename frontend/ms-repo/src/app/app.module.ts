import { NgModule, APP_INITIALIZER } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { CommonModule } from '@angular/common';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { FormsModule } from '@angular/forms';
import { HttpClientModule } from "@angular/common/http"
import { CardModule } from 'primeng/card';
import {
  DialogService,
  DynamicDialogModule,
  DynamicDialogRef,
} from 'primeng/dynamicdialog';
import { ButtonsModule } from 'ngx-bootstrap/buttons';
import { BsDropdownModule } from 'ngx-bootstrap/dropdown';
import { TableModule } from 'primeng/table';
import { DashboardComponent } from './dashboard/dashboard.component';
import { MapComponent } from './map/map.component';
import { SupportComponent } from './support/support.component';
import { DataService } from "./core/data.service"
import { DropdownModule } from 'primeng/dropdown';
import { TooltipModule } from 'primeng/tooltip';
import { InputTextModule } from 'primeng/inputtext';
import { NgxSpinnerModule } from 'ngx-spinner';
import { TableFilterModule } from './core/table-filter';
import { DialogModule } from 'primeng/dialog';
export function dataService(provider: DataService) {
  return () => provider.load();
}
@NgModule({
  declarations: [
    AppComponent,
    DashboardComponent,
    MapComponent,
    SupportComponent,
  ],
  imports: [
    BrowserModule,
    CommonModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    FormsModule,
    CardModule,
    ButtonsModule,
    BsDropdownModule,
    TableModule,
    HttpClientModule,
    DropdownModule,
    TooltipModule,
    InputTextModule,
    NgxSpinnerModule,
    TableFilterModule,
    DialogModule,
  ],
  providers: [
    DialogService,
    DynamicDialogRef,
    DataService,
    {
      provide: APP_INITIALIZER,
      useFactory: dataService,
      deps: [DataService],
      multi: true,
    },
  ],
  bootstrap: [AppComponent],
})
export class AppModule {}
