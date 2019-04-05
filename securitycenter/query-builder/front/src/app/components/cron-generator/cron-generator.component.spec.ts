import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import {
  MatFormFieldModule,
  MatSelectModule,
  MatInputModule,
  MatTooltipModule,
  MatCheckboxModule
} from '@angular/material';
import { FormsModule } from '@angular/forms';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import * as moment from 'moment-timezone';

import { CronGeneratorComponent } from './cron-generator.component';

describe('CronGeneratorComponent', () => {
  let component: CronGeneratorComponent;
  let fixture: ComponentFixture<CronGeneratorComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      imports: [
        MatFormFieldModule,
        MatSelectModule,
        MatInputModule,
        BrowserModule,
        BrowserAnimationsModule,
        FormsModule,
        MatTooltipModule,
        MatCheckboxModule
      ],
      declarations: [ CronGeneratorComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(CronGeneratorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('creates the component', () => {
    expect(component).toBeTruthy();
  });

  it('generates a cron expression to run hourly at minute 0 when change kind to Hour', () => {
    const expectedExpression = '0 */1 * * *';
    component.kind = { name: 'Hour', hourPrefix: '*/', dayPrefix: '' };
    component.kindChange();
    expect(component.value).toEqual(expectedExpression);
  });

  it('generates a cron expression with parameters set to run daily at 11:00', () => {
    const expectedExpression = '0 11 */1 * *';
    component.kind = { name: 'Day', hourPrefix: '', dayPrefix: '*/' };
    component.cron.hour = 11;
    component.cron.minute = 0;
    component.cron.dayOfMonth = 1;
    component.updateExpression();
    expect(component.value).toEqual(expectedExpression);
  });

  it('generates a expression with parameters to run every monday and friday at 5:00', () => {
    const expectedExpression = '0 5 * * 1,5';
    component.kind = { name: 'Week', hourPrefix: '', dayPrefix: '' };
    component.cron.hour = 5;
    component.cron.minute = 0;
    component.cron.dayOfWeek = [1, 5];
    component.updateExpression();
    expect(component.value).toEqual(expectedExpression);
  });

  it('simulates next executions with 2 hour difference between them', () => {
    component.value = '0 */2 * * *';
    component.generateNextExecutions();
    const execution2 = new Date(component.nextExecutions[1]);
    const execution3 = new Date(component.nextExecutions[2]);
    const diff = execution3.getHours() - execution2.getHours();
    expect(diff).toEqual(2);
  });

  it('simulates next executions with 3 days difference between them', () => {
    component.value = '0 17 */3 * *';
    component.generateNextExecutions();
    const execution2 = new Date(component.nextExecutions[1]);
    const execution3 = new Date(component.nextExecutions[2]);
    const diff = execution3.getDate() - execution2.getDate();
    expect(diff).toEqual(3);
  });

  it('does return array with "Monday, Tuesday" when day of week value is 1', () => {
    const expected = 'Monday, Tuesday';
    component.cron.dayOfWeek = [1, 2];
    expect(component.selectedWeekDays()).toEqual(expected);
  });

  it('does return hour kind building from expression', () => {
    const expected = { name: 'Hour', hourPrefix: '*/', dayPrefix: '' };
    component.value = '0 */2 * * *';
    expect(component.defineKindFromExpression()).toEqual(expected);
  });

  it('does return day kind building from expression', () => {
    const expected = { name: 'Day', hourPrefix: '', dayPrefix: '*/' };
    component.value = '0 11 */1 * *';
    expect(component.defineKindFromExpression()).toEqual(expected);
  });

  it('does return week kind building from expression', () => {
    const expected = { name: 'Week', hourPrefix: '', dayPrefix: '' };
    component.value = '0 11 * * 1,2';
    expect(component.defineKindFromExpression()).toEqual(expected);
  });

  it('simulate next executions with timezone', () => {
    const expected = 'Fri Jan 20 2012 11:51:36 GMT-0200';
    const test = new Date('Fri Jan 20 2012 10:51:36 GMT-0500').toString();
    const parsedDate = component.parseDate(test);
    expect(expected).toEqual(parsedDate);
  });
});
