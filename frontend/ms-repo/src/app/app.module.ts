import { NgModule, APP_INITIALIZER } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { CommonModule } from '@angular/common';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { FormsModule } from '@angular/forms';
import { HttpClientModule } from "@angular/common/http"
import { CardModule } from 'primeng/card';
import { ToastModule } from 'primeng/toast';
import { ButtonsModule } from 'ngx-bootstrap/buttons';
import { BsDropdownModule } from 'ngx-bootstrap/dropdown';
import { DashboardComponent } from './dashboard/dashboard.component';
import { SupportComponent } from './support/support.component';
import { DataService } from "./core/data.service"
import { InputTextModule } from 'primeng/inputtext';
import { FileUploadModule } from 'primeng/fileupload';
import { NgxSpinnerModule } from 'ngx-spinner';
import { MessageService } from 'primeng/api';

@NgModule({
  declarations: [AppComponent, DashboardComponent, SupportComponent],
  imports: [
    BrowserModule,
    CommonModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    FormsModule,
    CardModule,
    ButtonsModule,
    BsDropdownModule,
    HttpClientModule,
    InputTextModule,
    NgxSpinnerModule,
    FileUploadModule,
    ToastModule,
  ],
  providers: [DataService, MessageService],
  bootstrap: [AppComponent],
})
export class AppModule {}
