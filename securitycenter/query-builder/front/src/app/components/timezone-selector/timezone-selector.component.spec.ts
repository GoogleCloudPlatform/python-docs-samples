import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { TimezoneSelectorComponent } from './timezone-selector.component';
import { FormsModule } from '@angular/forms';
import {
  MatIconModule,
  MatFormFieldModule,
  MatAutocompleteModule,
  MatInputModule
} from '@angular/material';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import * as moment from 'moment-timezone';


describe('TimezoneSelectorComponent', () => {
  let component: TimezoneSelectorComponent;
  let fixture: ComponentFixture<TimezoneSelectorComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      imports: [
        FormsModule,
        MatFormFieldModule,
        MatAutocompleteModule,
        MatIconModule,
        MatInputModule,
        BrowserAnimationsModule
      ],
      declarations: [ TimezoneSelectorComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TimezoneSelectorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('creates the component timezone-selector', () => {
    expect(component).toBeTruthy();
  });

  it('selects an option', () => {
    component.optionSelected();
    expect(component.invalidSelection).toBeFalsy();
  });

  it('it does filter the timezones by a string', () => {
    component.filterTimeZones('brazil');
    expect(component.filteredTimeZones.length).toEqual(4);
  });

  it('has a default value', () => {
    component.forceValidSelection = true;
    component.setDefaultTz = true;
    component.ngOnInit();
    expect(component.tzModel).toMatch(moment.tz.guess());
  });

  it('does not set invalid for random text when focuses out without forceValidSelection ', () => {
    component.forceValidSelection = false;
    component.invalidSelection = false;
    component.onFocusOut(null);
    expect(component.invalidSelection).toBeFalsy();
  });

  it('does not set invalid for empty timezone when focuses out with forceValidSelection', () => {
    component.forceValidSelection = true;
    component.invalidSelection = false;
    component.tzModel = '';
    component.onFocusOut(null);
    expect(component.invalidSelection).toBeFalsy();
  });

  it('sets invalid for invalid timezone when focuses out with forceValidSelection', () => {
    component.forceValidSelection = true;
    component.invalidSelection = false;
    component.tzModel = 'blah';
    component.onFocusOut(null);
    expect(component.invalidSelection).toBeTruthy();
  });

  it('sets default timezone with handleDefaultValue', () => {
    const defaultTimeZone = moment.tz.guess();
    component.setDefaultTz = true;
    component.handleDefaultValue();
    expect(component.tzModel).toEqual(defaultTimeZone);
  });
});
