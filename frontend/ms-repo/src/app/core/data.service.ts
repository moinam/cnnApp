import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { NgxSpinnerService } from 'ngx-spinner';
import { MessageService } from 'primeng/api';

const httpOptions = {
  headers: new HttpHeaders({ 'Content-Type': 'application/json' }),
};

@Injectable({
  providedIn: 'root',
})
export class DataService {
  result: any;
  resAvail: boolean = false;
  serverUrl = 'http://localhost:8080'; //local setting
  //serverUrl = ''; //production setting
  constructor(private http: HttpClient, private spinner: NgxSpinnerService, private messageService: MessageService) {}

  /**
   * POST call to backend to fetch recognzied digit from the given image.
   *
   * @param {file} file Image File to be added to the post call
   *
   * @memberOf DataService
   */
  getRecognition(file: any): any {
    this.spinner.show();
    this.http
      .post(this.serverUrl + '/recognize', file)
      .subscribe((value: any) => {
        this.result = value;
        this.resAvail = true;
        console.log(this.result.Prediction);
        this.spinner.hide();
      },
      (error) => {
        this.messageService.add({
          severity: 'error',
          summary: error.status + ' ' + error.statusText,
          detail: error.error.message,
        });
        this.spinner.hide();
      });
  }
}
