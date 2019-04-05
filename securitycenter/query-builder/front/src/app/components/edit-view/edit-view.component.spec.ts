import { async, ComponentFixture, TestBed, inject } from '@angular/core/testing';
import { EditViewComponent } from './edit-view.component';
import { CronGeneratorComponent } from '../cron-generator/cron-generator.component';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { RouterModule, ActivatedRoute } from '@angular/router';
import { HttpClientModule } from '@angular/common/http';
import {
  MatToolbarModule,
  MatCardModule,
  MatIconModule,
  MatListModule,
  MatMenuModule,
  MatFormFieldModule,
  MatSelectModule,
  MatInputModule,
  MatAutocompleteModule,
  MatPaginatorModule,
  MatSnackBarModule,
  MatTooltipModule,
  MatCheckboxModule,
  MatSlideToggleModule,
  MatDialogModule
} from '@angular/material';
import { MatExpansionModule } from '@angular/material/expansion';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { OwlDateTimeModule, OwlNativeDateTimeModule } from 'ng-pick-datetime';
import { TimezoneSelectorComponent } from '../timezone-selector/timezone-selector.component';
import { AppRoutes } from '../../app.routing';
import { ListViewComponent } from '../list-view/list-view.component';
import { APP_BASE_HREF } from '@angular/common';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { Query } from '../../models/query';
import { Step } from '../../models/step';

describe('EditViewComponent', () => {
  let component: EditViewComponent;
  let fixture: ComponentFixture<EditViewComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      imports: [
        MatToolbarModule,
        MatCardModule,
        MatIconModule,
        MatListModule,
        MatMenuModule,
        MatFormFieldModule,
        MatSelectModule,
        MatInputModule,
        BrowserModule,
        BrowserAnimationsModule,
        RouterModule.forRoot(AppRoutes),
        FormsModule,
        ReactiveFormsModule,
        OwlDateTimeModule,
        MatAutocompleteModule,
        HttpClientModule,
        MatPaginatorModule,
        OwlNativeDateTimeModule,
        MatSnackBarModule,
        MatProgressSpinnerModule,
        MatExpansionModule,
        MatTooltipModule,
        MatCheckboxModule,
        MatSlideToggleModule,
        MatDialogModule
      ],
      declarations: [ EditViewComponent, TimezoneSelectorComponent, ListViewComponent, CronGeneratorComponent ],
      providers: [ { provide: APP_BASE_HREF, useValue : '/' }, ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(EditViewComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  this.fillStepThreshold = function(stepIndex: number, value: number, operator: string) {
    component.query.steps[stepIndex].threshold.value = value;
    component.query.steps[stepIndex].threshold.operator = operator;
  };

  it('creates the component edit-view', () => {
    expect(component).toBeTruthy();
  });

  it('verifies if an object is empty', () => {
    expect(component.isEmptyObject({})).toBeTruthy();
  });

  it('assigns an object query to the component', () => {
    // Given this
    const response = {
      data : {
        name: 'name',
        description: 'desc',
        steps: [],
        topic: 'topic',
        uuid: 'uuid',
        owner: 'owner',
      }
    };
    const query = new Query('name', 'desc', [], 'topic', 'uuid', 'owner');
    // Do this
    component.assignQuery(response);
    // Expect this
    expect(component.query).toEqual(query);
  });

  it('assigns the steps to the component query object', () => {
    // Given this
    const step = new Step();
    const response = {
      data : {
        steps: [step, step],
      }
    };
    const steps = [step, step];
    // Do this
    component.assignSteps(response);
    // Expect this
    expect(component.query.steps).toEqual(steps);
  });

  it('adds a new step to the form', () => {
    // Given this
    component.addNewStep(2);
    // Expect this
    expect(component.query.steps.length).toBeGreaterThan(1);
  });

  it('deletes a step that was previously added', () => {
    // Given this
    component.addNewStep(2);
    // Do this
    component.deleteStep(1);
    // Expect this
    expect(component.query.steps.length).toEqual(1);
  });

  it('enables the run button with one step and threshold filled', () => {
    this.fillStepThreshold(0, 1, '>=');
    expect(component.disableRunButton()).toBeFalsy();
  });

  it('disables the run button with one step and threshold value empty', () => {
    this.fillStepThreshold(0, null, '>=');
    expect(component.disableRunButton()).toBeTruthy();
  });

  it('enables the run button with one step and threshold operator empty', () => {
    this.fillStepThreshold(0, 1, null);
    expect(component.disableRunButton()).toBeTruthy();
  });

  it('disables the run button with two steps and empty joins', () => {
    // Given this
    component.addNewStep(2);
    this.fillStepThreshold(0, 1, '>=');
    this.fillStepThreshold(1, 2, '=');
    // Expect this
    expect(component.disableRunButton()).toBeTruthy();
  });

  it('enables the run button with two steps and filled joins', () => {
    // Given this
    component.addNewStep(2);
    this.fillStepThreshold(0, 1, '>=');
    this.fillStepThreshold(1, 2, '=');
    // Do this
    component.query.steps[0].setJoins('', 'outJoin1');
    component.query.steps[1].setJoins('inJoin2', '');
    // Expect this
    expect(component.disableRunButton()).toBeFalsy();
  });

  it('disables the run button with two steps and filled joins but missing one threshold value', () => {
    // Given this
    component.addNewStep(2);
    this.fillStepThreshold(0, null, '>=');
    this.fillStepThreshold(1, 2, '=');
    // Do this
    component.query.steps[0].setJoins('', 'outJoin1');
    component.query.steps[1].setJoins('inJoin2', '');
    // Expect this
    expect(component.disableRunButton()).toBeTruthy();
  });

  it('disables the run button with two steps and wrong filled joins', () => {
    // Given this
    component.addNewStep(2);
    this.fillStepThreshold(0, 1, '>=');
    this.fillStepThreshold(1, 2, '=');
    // Do this
    component.query.steps[0].setJoins('inJoin1', '');
    component.query.steps[1].setJoins('', 'outJoin2');
    // Expect this
    expect(component.disableRunButton()).toBeTruthy();
  });

  it('enables the run button with three steps and filled joins', () => {
    // Given this
    component.addNewStep(2);
    component.addNewStep(3);
    this.fillStepThreshold(0, 1, '>=');
    this.fillStepThreshold(1, 2, '=');
    this.fillStepThreshold(2, 3, '<=');
    // Do this
    component.query.steps[0].setJoins('', 'outJoin1');
    component.query.steps[1].setJoins('inJoin2', 'outJoin2');
    component.query.steps[2].setJoins('inJoin3', '');
    // Expect this
    expect(component.disableRunButton()).toBeFalsy();
  });

  it('disables the run button with three steps and filled joins but missing one threshold operator', () => {
    // Given this
    component.addNewStep(2);
    component.addNewStep(3);
    this.fillStepThreshold(0, 1, null);
    this.fillStepThreshold(1, 2, '=');
    this.fillStepThreshold(2, 3, '<=');
    // Do this
    component.query.steps[0].setJoins('', 'outJoin1');
    component.query.steps[1].setJoins('inJoin2', 'outJoin2');
    component.query.steps[2].setJoins('inJoin3', '');
    // Expect this
    expect(component.disableRunButton()).toBeTruthy();
  });

  it('disables the run button with three steps and wrong filled joins', () => {
    // Given this
    component.addNewStep(2);
    component.addNewStep(3);
    this.fillStepThreshold(0, 1, '>=');
    this.fillStepThreshold(1, 2, '=');
    this.fillStepThreshold(2, 3, '<=');
    // Do this
    component.query.steps[0].setJoins('inJoin1', '');
    component.query.steps[1].setJoins('', 'outJoin2');
    component.query.steps[2].setJoins('inJoin3', '');
    // Expect this
    expect(component.disableRunButton()).toBeTruthy();
  });

  it('disables the run button with three steps and empty joins', () => {
    // Given this
    component.addNewStep(2);
    component.addNewStep(3);
    this.fillStepThreshold(0, 1, '>=');
    this.fillStepThreshold(1, 2, '=');
    this.fillStepThreshold(2, 3, '<=');
    // Expect this
    expect(component.disableRunButton()).toBeTruthy();
  });

  it('shows the scc link on another tab', () => {
    // Given this
    component.sccLink = 'https://www.google.com/';
    const view = component.viewResultsOnConsole;
    // Do this
    spyOn(component, 'viewResultsOnConsole').and.callThrough();
    component.viewResultsOnConsole();
    // Expect this
    expect(component.viewResultsOnConsole).toHaveBeenCalled();
  });

});
