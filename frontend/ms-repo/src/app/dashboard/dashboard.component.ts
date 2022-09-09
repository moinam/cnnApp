import { Component, OnInit } from '@angular/core';
import { DataService } from '../core/data.service';
import { NgxSpinnerService } from 'ngx-spinner';
import { MessageService } from 'primeng/api';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css'],
})
export class DashboardComponent implements OnInit {
  filterCriteria: any;
  uploadedFile: any;
  constructor(
    public dataService: DataService,
    private messageService: MessageService
  ) {}

  ngOnInit(): void {}

  onUpload(event: any) {
    this.uploadedFile = event.files[0];
    this.messageService.add({
      severity: 'info',
      summary: 'Success',
      detail: 'File Uploaded',
    });
    console.log(this.uploadedFile);
  }

  reset() {
    this.uploadedFile = null;
    this.dataService.resAvail = false;
  }

  getPrediction() {
    this.dataService.getRecognition(this.uploadedFile);
  }
}
