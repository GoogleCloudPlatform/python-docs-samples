import { async, ComponentFixture, TestBed, fakeAsync, tick, discardPeriodicTasks } from '@angular/core/testing';
import { RouterModule, ActivatedRoute } from '@angular/router';
import { APP_BASE_HREF } from '@angular/common';
import {
  MatToolbarModule,
  MatCardModule,
  MatIconModule,
  MatListModule,
  MatMenuModule,
  MatInputModule,
  MatFormFieldModule,
  MatSelectModule,
  MatDialogModule,
  MatSnackBarModule,
  MatPaginatorModule,
  MatAutocompleteModule,
  MatTooltipModule,
  MatCheckboxModule,
  MatSlideToggleModule
} from '@angular/material';
import { MatExpansionModule } from '@angular/material/expansion';
import { HttpClientModule } from '@angular/common/http';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { OwlDateTimeModule } from 'ng-pick-datetime';

import { ListViewComponent } from './list-view.component';
import { CronGeneratorComponent } from '../cron-generator/cron-generator.component';
import { EditViewComponent } from '../edit-view/edit-view.component';
import { AppRoutes } from '../../app.routing';
import { TimezoneSelectorComponent } from '../timezone-selector/timezone-selector.component';
import { SimpleQuery } from '../../models/simple-query';
import { environment } from '../../../environments/environment';
import { SimpleQueryResult } from '../../models/simple-query-result';
import { LastExecution } from '../../models/last-execution';

describe('ListViewComponent', () => {
  let component: ListViewComponent;
  let fixture: ComponentFixture<ListViewComponent>;
  let backend: HttpTestingController;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      imports: [
        MatToolbarModule,
        MatCardModule,
        MatIconModule,
        MatListModule,
        MatMenuModule,
        RouterModule.forRoot(AppRoutes),
        MatInputModule,
        MatFormFieldModule,
        MatSelectModule,
        MatDialogModule,
        MatSnackBarModule,
        ReactiveFormsModule,
        FormsModule,
        MatPaginatorModule,
        MatAutocompleteModule,
        OwlDateTimeModule,
        HttpClientModule,
        MatProgressSpinnerModule,
        BrowserAnimationsModule,
        MatExpansionModule,
        MatTooltipModule,
        MatCheckboxModule,
        MatSlideToggleModule,
        HttpClientTestingModule
      ],
      declarations: [
        ListViewComponent,
        EditViewComponent,
        TimezoneSelectorComponent,
        CronGeneratorComponent
      ],
      providers: [
        { provide: APP_BASE_HREF, useValue : '/' },
        { provide: ActivatedRoute, useValue: {
          data: {
            subscribe: (data: any) => data({
              data: {
                total: 0,
                queries: []
              }
            })
          }
        }}
      ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ListViewComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
    backend = TestBed.get(HttpTestingController);
  });

  it('creates the component list-view', () => {
    expect(component).toBeTruthy();
  });

  it('shows text search', () => {
    component.searchClickAction();
    expect(component.showInput).toBeTruthy();
  });

  it('hides text search', () => {
    component.showInput = true;
    component.searchClickAction();
    expect(component.showInput).toBeFalsy();
  });

  it('changes page size', () => {
    const searchEvent = { previousPageIndex: 0, pageIndex: 0, pageSize: 25, length: 0};
    component.onPageEvent(searchEvent);
    expect(component.paginatorObj.pageSize).toEqual(25);
  });

  it('changes current page', () => {
    const searchEvent = { previousPageIndex: 0, pageIndex: 1, pageSize: 25, length: 0};
    component.onPageEvent(searchEvent);
    expect(component.paginatorObj.currentPage).toEqual(2);
  });

  it('getQueries() returns queries', fakeAsync(() => {
    const lastExecution = new LastExecution('2018-07-07T04:41:00');
    const query = new SimpleQuery('Query 1', 'Lorem ipsum sit dolor amet.', '04/03/1990', 1, 'thulio', '2018-07-07T04:41:00', null, null, lastExecution);
    const mockObj = new SimpleQueryResult([query, query], 1);
    const page = {
      currentPage: 1,
      pageSize: 10
    };
    component.textSearchControl.setValue('teste');

    component.getQueries();
    const mock = backend.expectOne(`${environment.apiUrl}/queries?page=${page.currentPage}&page_size=${page.pageSize}&text=${component.textSearchControl.value}`);

    expect(mock.request.method).toEqual('GET');

    mock.flush(mockObj);
    tick();

    expect(component.queriesResult).toEqual(mockObj);
    discardPeriodicTasks();
  }));
});
