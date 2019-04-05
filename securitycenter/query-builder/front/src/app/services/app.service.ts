import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class AppService {

  private toolbarInfo;

  constructor() { }

  public setToolbarInfo(title) {
    this.toolbarInfo = title;
  }

  public getToolbarInfo() {
    return this.toolbarInfo;
  }
}
