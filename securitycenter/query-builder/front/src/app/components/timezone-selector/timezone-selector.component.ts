import { Component, Input, Output, EventEmitter, OnInit } from '@angular/core';
import * as moment from 'moment-timezone';

@Component({
  selector: 'qb-timezone-selector',
  templateUrl: './timezone-selector.component.html',
  styleUrls: ['./timezone-selector.component.scss']
})
export class TimezoneSelectorComponent implements OnInit {

  timeZones: any;
  filteredTimeZones: any;
  tzModel: string;
  tzSelectedValue: string;
  invalidSelection: boolean;

  @Input() placeholderText: string;
  @Input() forceValidSelection: boolean;
  @Input() disabled: boolean;
  @Input() model: string;
  @Input() setDefaultTz: boolean;
  @Output() tzSelected = new EventEmitter<string>();

  constructor() {
    this.timeZones = moment.tz.names();
    this.filteredTimeZones = this.timeZones;
  }

  ngOnInit(): void {
    if (this.setDefaultTz) {
      this.tzModel = this.model || moment.tz.guess();
    } else {
      this.tzModel = this.model;
    }
    this.onFocusOut(null);
  }

  optionSelected(): void {
    this.tzSelectedValue = this.tzModel;
    this.invalidSelection = false;
    this.tzSelected.emit(this.tzModel);
  }

  filterTimeZones(name: string) {
    this.filteredTimeZones = this.timeZones.filter(timeZone =>
      timeZone.toLowerCase().indexOf(name.toLowerCase()) !== -1);
  }

  onFocusOut(form) {
    if (this.forceValidSelection) {
      if (!this.tzModel) {
        this.handleDefaultValue();
        this.optionSelected();
        this.invalidSelection = false;
      } else {
        if (this.timeZones.indexOf(this.tzModel) === -1) {
          this.invalidSelection = true;
          this.tzSelectedValue = '';
        }
      }
    }
  }

  handleDefaultValue() {
    if (this.setDefaultTz) {
      this.tzModel = moment.tz.guess();
    }
  }
}
