import { Component, OnInit, ViewChild, ElementRef } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { MatDialog,
         MatSnackBar,
         MatExpansionPanel
} from '@angular/material';

import { AppService } from '../../services/app.service';
import { QueryService } from '../../services/query.service';
import { FormControl } from '@angular/forms';
import { debounceTime } from 'rxjs/operators';
import { SimpleQueryResult } from '../../models/simple-query-result';
import * as moment from 'moment-timezone';
import { ConfirmDialogViewComponent } from '../confirm-dialog/confirm-dialog.component';
import {SessionErrorHandler} from '../../handlers/session-error-handler';

@Component({
  selector: 'qb-list-view',
  templateUrl: './list-view.component.html',
  styleUrls: ['./list-view.component.scss']
})
export class ListViewComponent implements OnInit {

  @ViewChild('searchInput') searchInput: ElementRef;

  showPaginator = true;
  queriesResult: SimpleQueryResult;
  paginatorObj: any;
  showInput: boolean;
  textSearchControl = new FormControl();
  queryRunning: number;
  toggleRunning: boolean;

  constructor (private appService: AppService, private route: ActivatedRoute,
    public dialog: MatDialog,
    private queryService: QueryService,
    private sessionErrorHandler: SessionErrorHandler,
    public snackBar: MatSnackBar) {
      this.appService.setToolbarInfo({title: 'Query list', route: undefined});
      this.showInput = false;
  }

  ngOnInit(): void {
    this.route.data.subscribe((data: any) => {
      if (data.error) {
        this.sessionErrorHandler.handleExpiredSession(new Error(data.error));
      } else {
        this.queriesResult = data.data;
        this.parseDates();
    }});

    this.paginatorObj = {
      pageSize: 10,
      resultSize: this.queriesResult.total,
      pageSizeOptions: [10, 25, 50, 100],
      currentPage: 1
    };

    this.textSearchControl.valueChanges.pipe(debounceTime(1000))
      .subscribe((newValue) => {
        this.showPaginator = false;
        this.onPageEvent({});
      });
  }


  expandPanelControl(matExpansionPanel: MatExpansionPanel, event: Event): void {
    event.stopPropagation();

    if (!this._isExpansionIndicator(event.target)) {
      matExpansionPanel.close();
    }
  }

  private _isExpansionIndicator(target): boolean {
    const expansionIndicatorClass = 'expansion-indicator';
    return (target.classList && target.classList.contains(expansionIndicatorClass) || target.classList.contains('ng-trigger'));
  }

  getQueries() {
    this.queryService.getQueryList(this.paginatorObj.currentPage, this.paginatorObj.pageSize, this.textSearchControl.value)
      .then(response => {
        this.queriesResult = response;
        this.parseDates();
        this.paginatorObj.resultSize = response.total;
        this.showPaginator = true;
      })
      .catch((err) => {
        this.queryRunning = null;
        this.sessionErrorHandler.handleExpiredSession(err);
      });
  }

  parseDates() {
    if (this.queriesResult.queries && this.queriesResult.queries.length) {
      const format = 'ddd MMM DD YYYY HH:mm:ss G\\MTZZ';
      this.queriesResult.queries.forEach(item => {
        if (item.nextRun) {
          const nextExecution = moment.tz(item.nextRun, 'UTC').tz(moment.tz.guess());
          item.nextRun = nextExecution.format(format);
        }
        if (item.lastExecution && item.lastExecution.date) {
          const lastExecutionDate = moment.tz(item.lastExecution.date, 'UTC').tz(moment.tz.guess());
          item.lastExecution.date = lastExecutionDate.format(format);
        }
        const lastUpdated = moment.tz(item.timestamp, 'UTC').tz(moment.tz.guess());
        item.timestamp = lastUpdated.format(format);
      });
    }
  }

  searchClickAction(): void {
    this.showInput = !this.showInput;
    if (!this.showInput) {
      this.textSearchControl.setValue(null);
    } else {
      setTimeout(() => {
        this.searchInput.nativeElement.focus();
      }, 300);
    }
  }

  onPageEvent(event) {
    const pageIndex = event.pageIndex ? event.pageIndex + 1 : 1;
    this.paginatorObj.currentPage = pageIndex;
    this.paginatorObj.pageSize = event.pageSize || this.paginatorObj.pageSize;
    this.getQueries();
  }

  openDialog(queryId, queryName): void {
    const dialogRef = this.dialog.open(ConfirmDialogViewComponent, {
      width: '35%',
      data: {
        confirmTitle: 'Are you sure...',
        confirmMessage: 'Do you really want to delete this query named <strong>' + queryName + '</strong>?',
        cancelButtonText: 'NO, CANCEL',
        confirmButtonText: 'YES, DELETE'
      }
    });

    dialogRef.afterClosed().subscribe(isConfirmed => {
      if (isConfirmed) {
        this.queryService.deleteQuery(queryId).then(() => {
          const snackRef = this.snackBar.open('Query deleted successfully', 'OK', { duration: 2000 });
          snackRef.afterDismissed().subscribe(() => {
            this.getQueries();
          });
        })
        .catch((err) => {
          this.sessionErrorHandler.handleExpiredSession(err);
        });
      }
    });
  }

  runQuery(queryId, index): void {
    this.queryRunning = index;
    this.queryService.runQueryById(queryId).then(response => {
      const snackBarMessage = response['result_size'] + ' items to be marked. Filter results on console with the mark "' + response['mark'] + '".';
      const snackRef = this.snackBar.open(snackBarMessage, 'OPEN IN CONSOLE', { duration: 30000 });
      this.queryRunning = null;
      this.getQueries();
      snackRef.onAction().subscribe(function() {
        window.open(response['scc_query_link'], '_blank');
      });
    })
    .catch((err) => {
      this.queryRunning = null;
      this.sessionErrorHandler.handleExpiredSession(err);
    });
  }

  toggleNotification(query) {
    let snackMessage = 'Query notification disabled.';
    if (query.sendNotification) {
      snackMessage = 'Query notification enabled.';
    }
    this.queryService.toggleNotification(query.uuid, query.sendNotification).then(response => {
      this.snackBar.open(snackMessage, 'OK', { duration: 2000 });
      this.getQueries();
    })
    .catch(err => {
      query.sendNotification = !query.sendNotification;
      this.sessionErrorHandler.handleExpiredSession(err);
    });
  }

}
