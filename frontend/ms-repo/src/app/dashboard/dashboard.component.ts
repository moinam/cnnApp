import { Component, OnInit } from '@angular/core';
import { DataService } from '../core/data.service';
import { NgxSpinnerService } from 'ngx-spinner';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css'],
})
export class DashboardComponent implements OnInit {
  selectedClient: any;
  selectedTaskType: any;
  quantity: any;
  search: any = '';
  teams: any;
  filterCriteria: any;
  dispMap: boolean = false;
  currentClient: any;
  clientLocation: any;
  teamLocation: any;
  map_url = '';
  constructor(
    public dataService: DataService,
    private spinner: NgxSpinnerService
  ) {
    this.filterCriteria = {
      clientId: '',
      taskType: '',
      quantity: '',
    };

    this.dataService.locationReady.subscribe((load: boolean) => {
      if (load) {
        console.log(this.dataService.clientLocation);
        console.log(this.dataService.teamLocation);
        this.map_url =
          'https://maps.googleapis.com/maps/api/staticmap?size=650x350&maptype=roadmap&markers=color:blue%7Clabel:C%7C' +
          this.dataService.clientLocation.lat +
          ',' +
          this.dataService.clientLocation.lng +
          '&markers=color:green%7Clabel:T%7C' +
          this.dataService.teamLocation.lat +
          ',' +
          this.dataService.teamLocation.lng +
          '&key=' +
          this.dataService.map_config.key;
        this.dispMap = true;
        this.spinner.hide();
        this.dataService.locationReady.next(false);
      }
    });
  }

  ngOnInit(): void {}

  getDate(timestamp: any): any {
    let hours = Math.floor(timestamp / 60 / 60);
    let minutes = Math.floor(timestamp / 60) - hours * 60;
    let formatted = '';
    if (hours > 0) {
      formatted += hours.toString() + ' Hrs';
      if (minutes > 0){
        formatted += ' and ';
      }
    }
    if (minutes > 0) {
      formatted += minutes.toString() + ' min ';
    }
    return formatted;
  }

  getPrediction(): any {
    this.currentClient = this.selectedClient;
    this.filterCriteria.clientId = this.selectedClient.clientId;
    this.filterCriteria.taskType = this.selectedTaskType;
    this.filterCriteria.quantity = this.quantity;
    console.log(this.filterCriteria);
    console.log('Hit!!');
    this.dataService.getTeams(this.filterCriteria);
  }
  showMap(team: any) {
    this.spinner.show();
    this.clientLocation = this.dataService.fetchGeoLocation(
      this.currentClient.location,
      team.location
    );
  }

  reset(): any {
    this.selectedClient = null;
    this.selectedTaskType = null;
    this.quantity = null;
  }
}
