import { Component } from '@angular/core';
import { AppService } from './services/app.service';

@Component({
  selector: 'qb-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'app';
  constructor (private appService: AppService) {}

  getToolbarInfo() {
    return this.appService.getToolbarInfo();
  }
}
