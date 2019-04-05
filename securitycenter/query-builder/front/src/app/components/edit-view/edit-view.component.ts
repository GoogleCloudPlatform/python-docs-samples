import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { MatSnackBar, MatMenuTrigger, MatDialog } from '@angular/material';

import { AppService } from '../../services/app.service';
import { Query } from '../../models/query';
import { Step } from '../../models/step';
import { ReadTime } from '../../models/read-time';
import { QueryService } from '../../services/query.service';
import { ExecutionResult } from '../../models/execution-result';
import { ConfirmDialogViewComponent } from '../confirm-dialog/confirm-dialog.component';
import {SessionErrorHandler} from '../../handlers/session-error-handler';
import * as moment from 'moment-timezone';


@Component({
  selector: 'qb-edit-view',
  templateUrl: './edit-view.component.html',
  styleUrls: ['./edit-view.component.scss']
})
export class EditViewComponent implements OnInit {

  query: Query;
  fieldsReadOnly: boolean;
  resultMessage: string;
  resultCode: string;
  sccLink: string;
  queryRunning: boolean;
  runResult: ExecutionResult;
  scheduleQuery = false;
  userExecutionTz = null;
  genericErrorMessage = 'Some error ocurred, please try again or contact support.';

  private kinds = [
    {displayName: 'Asset', value: 'ASSET'},
    {displayName: 'Finding', value: 'FINDING'}
  ];
  private readTimeTypes = [
    {displayName: 'Timestamp', value: 'TIMESTAMP'},
    {displayName: 'From now', value: 'FROM_NOW'}
  ];
  operators = [
    {displayName: 'Less than', value: 'lt'},
    {displayName: 'Less or equal', value: 'le'},
    {displayName: 'Equal', value: 'eq'},
    {displayName: 'Not equal', value: 'ne'},
    {displayName: 'Greater or equal', value: 'ge'},
    {displayName: 'Greater than', value: 'gt'}
  ];

  constructor(private appService: AppService,
              private queryService: QueryService,
              private route: ActivatedRoute,
              public snackBar: MatSnackBar,
              private router: Router,
              private sessionErrorHandler: SessionErrorHandler,
              public dialog: MatDialog) {
    this.appService.setToolbarInfo({title: 'Query builder', route: ''});
  }

  ngOnInit(): void {
    this.route.data
    .subscribe((response: any) => {
      if (!response.data) {
        this.query = new Query();
        this.addNewStep(null);
        this.fieldsReadOnly = false;
      } else {
        if (this.isEmptyObject(response.data)) {
          this.router.navigate(['query']);
          setTimeout(() => {
            this.snackBar.open('Query not found for the given id, opening new form.', 'OK', { duration: 5000 });
          }, 500);
        } else {
          this.assignQuery(response);
          this.assignSteps(response);
          this.fieldsReadOnly = true;
        }
      }
    });
  }

  isEmptyObject(obj): boolean {
    return Object.keys(obj).length === 0;
  }

  assignQuery(responseData): void {
    this.query = new Query();
    Object.assign(this.query, responseData.data);
    this.query.schedule ? this.scheduleQuery = true : this.scheduleQuery = false;
    if (responseData.data.lastExecution) {
      this.userExecutionTz = moment.tz(responseData.data.lastExecution.date, 'UTC').tz(moment.tz.guess());
    }
  }

  assignSteps(responseData): void {
    this.query.steps = new Array<Step>();
    responseData.data.steps.forEach(foundStep => {
      const newStep = new Step();
      Object.assign(newStep, foundStep);
      newStep.readTime = this.assignReadTime(newStep.readTime);
      this.query.steps.push(newStep);
    });
  }

  assignReadTime(originalData): ReadTime {
    const newRefTime = new ReadTime();
    Object.assign(newRefTime, originalData);
    newRefTime.momentValue = null;
    newRefTime.fillMomentTime();
    return newRefTime;
  }

  addNewStep(stepOrder): void {
    const step = new Step(stepOrder || 1, null, null, null, '', '', null);
    this.query.addStep(step);
    this.runResult = null;
  }

  saveQuery(form): void {
    if (form.valid) {
      this.query.toPayload(!this.scheduleQuery);
      this.queryService.saveQuery(this.query).then(() => {
        const snackRef = this.snackBar.open('Query saved successfully', 'OK', { duration: 2500 });
        snackRef.afterDismissed().subscribe(() => {
          this.fieldsReadOnly = true;
          this.router.navigate(['']);
        });
      })
      .catch((err) => {
        this.sessionErrorHandler.handleExpiredSession(err);
        err.status === 400 ? this.assignErrors(form, err.error) : this.setGeneralError(err.message);
      });
    }
  }

  stepResultMouseEnter(trigger: MatMenuTrigger) {
    trigger.openMenu();
  }

  stepResultMouseLeave(trigger: MatMenuTrigger, ev) {
    trigger.closeMenu();
    ev.srcElement.blur();
  }

  runQuery(form): void {
    this.query.toPayload(!this.scheduleQuery);
    this.queryRunning = true;
    this.resultMessage = null;
    this.runResult = null;
    this.sccLink = null;
    this.queryService.runQuery(this.query, !this.fieldsReadOnly).then(response => {
      this.resultMessage = response['result_size'] + ' items to be marked. Filter results on console with the mark "' + response['mark'] + '".';
      this.sccLink = response['scc_query_link'];
      this.query.uuid = response.uuid;
      this.queryRunning = false;
      this.runResult = response;
      setTimeout(() => {
        window.scrollTo(0, document.body.scrollHeight);
      }, 100);
    })
    .catch(response => {
      this.queryRunning = false;
      this.sessionErrorHandler.handleExpiredSession(response, true);
      response.status === 400 ? this.assignErrors(form, response.error) : this.setGeneralError(response.message);
    });
  }

  setGeneralError(message) {
    this.resultMessage = 'Unexpected error: ';
    this.resultMessage += message;
  }

  assignErrors(form, errors): void {
    const fieldsWithErrors = Object.keys(errors);
    fieldsWithErrors.forEach(fieldName => {
      const errorMessage = errors[fieldName].message;
      form.controls[fieldName].setErrors({ runError: true, runErrorMessage: errorMessage });
      form.controls[fieldName].touched = true;
    });
  }

  deleteStep(stepIndex): void {
    this.query.deleteStep(stepIndex);
  }

  disableRunButton(): boolean {
    const steps = this.query.steps;
    return !steps.every(this.validateStep, this);
  }

  validateStep(this, step, stepIndex, steps): boolean {
    if (!step.threshold || !step.threshold.value || !step.threshold.operator) {
      return false;
    }
    return steps.length === 1 || this.verifyJoins(step, stepIndex, steps);
  }

  verifyJoins(step, stepIndex, steps): boolean {
    switch (stepIndex) {
      case (0):
        return step.verifyJoins('outJoin');
      case (steps.length - 1):
        return step.verifyJoins('inJoin');
      default:
        return step.verifyJoins('inJoin') && step.verifyJoins('outJoin');
    }
  }

  onTimezoneSelect(timezone: string, readTime: ReadTime) {
    readTime.timeZone = timezone;
    readTime.updateTimezone();
  }

  viewResultsOnConsole(): void {
    window.open(this.sccLink);
  }

  dateSelected(readTime: ReadTime, readTimeValueModel) {
    let invalidReadTimeValue = null;
    if (readTimeValueModel.errors && readTimeValueModel.errors.owlDateTimeParse) {
      invalidReadTimeValue = readTimeValueModel.errors.owlDateTimeParse.text;
    }
    readTime.updateDate(invalidReadTimeValue);
  }

  canDeactivate() {
    if (!this.fieldsReadOnly) {
      const dialogRef = this.dialog.open(ConfirmDialogViewComponent, {
        width: '35%',
        data: {
          afterCloseEvent: 'afterCloseAction',
          confirmTitle: 'Are you sure...',
          confirmMessage: 'Do you want to discard the changes?'
        }
      });

      dialogRef.afterClosed().subscribe(isConfirmed => {
        if (isConfirmed && this.query.uuid) {
          this.queryService.cleanUpTempMarks(this.query.uuid);
        }
      });
      return dialogRef.afterClosed();
    }

    return true;
  }
}
