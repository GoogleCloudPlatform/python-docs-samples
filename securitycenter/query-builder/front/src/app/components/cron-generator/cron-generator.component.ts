import { Component, Input, OnInit } from '@angular/core';
import { NG_VALUE_ACCESSOR } from '@angular/forms';
import * as cronParser from 'cron-parser';
import { Cron } from '../../models/cron';
import { ValueAccessorBase } from '../../app-value-accessor';
import * as moment from 'moment-timezone';

@Component({
  selector: 'qb-cron-generator',
  templateUrl: './cron-generator.component.html',
  styleUrls: ['./cron-generator.component.scss'],
  providers: [{
    provide: NG_VALUE_ACCESSOR,
    useExisting: CronGeneratorComponent,
    multi: true
  }]
})
export class CronGeneratorComponent extends ValueAccessorBase<string> {

  @Input() readOnly: boolean;

  cron: Cron;
  kind: any;
  cronExpression: string;
  nextExecutions;
  showNextExecutions = false;
  kinds = [];
  minutes = [];
  hours = [];
  days = [];

  constructor() {
    super();
    this.kinds = [
      { name: 'Hour', hourPrefix: '*/', dayPrefix: '' },
      { name: 'Day', hourPrefix: '', dayPrefix: '*/' },
      { name: 'Week', hourPrefix: '', dayPrefix: '' }
    ];
    this.days = [
      { name: 'Sunday', value: 0 },
      { name: 'Monday', value: 1 },
      { name: 'Tuesday', value: 2 },
      { name: 'Wednesday', value: 3 },
      { name: 'Thursday', value: 4 },
      { name: 'Friday', value: 5 },
      { name: 'Saturday', value: 6 }
    ];
    for (let index = 0; index < 60; index++) {
      this.minutes.push(index);
      if (index <= 23) {
        this.hours.push(index);
      }
    }
    this.kind = this.kinds[0];
    this.cron = new Cron(this.kind.name);
    setTimeout(() => {
      if (this.value) {
        this.cron.buildFromExpression(this.value);
        this.kind = this.defineKindFromExpression();
      }

      this.updateExpression();
    }, 100);
  }

  defineKindFromExpression() {
    const cronArray = this.value.split(' ');
    if (cronArray[4] !== '*') {
      return this.kinds[2];
    } else if (cronArray[2] !== '*') {
      return this.kinds[1];
    }
    return this.kinds[0];
  }

  kindChange() {
    this.cron = new Cron(this.kind.name);
    this.showNextExecutions = false;
    this.updateExpression();
  }

  generateNextExecutions() {
    const interval = cronParser.parseExpression(this.value, {tz: 'UTC'});
    this.nextExecutions = [
      this.parseDate(interval.next().toString()),
      this.parseDate(interval.next().toString()),
      this.parseDate(interval.next().toString())
    ];
  }

  updateExpression() {
    this.value = this.cron.generateExpression(this.kind);
  }

  selectedWeekDays() {
    const selectedDays = [];
    this.cron.dayOfWeek.forEach(day => {
      this.days.filter(dayObj => {
        if (dayObj.value === day) {
          return selectedDays.push(dayObj.name);
        }
      });
    });
    return selectedDays.join(', ');
  }

  parseDate(date) {
    const format = 'ddd MMM DD YYYY HH:mm:ss G\\MTZZ';
    const nextExecution = moment.tz(date, 'UTC').tz(moment.tz.guess());
    return nextExecution.format(format);
  }

}
