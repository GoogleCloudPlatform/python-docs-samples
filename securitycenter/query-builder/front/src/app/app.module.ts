import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { NgModule } from '@angular/core';
import { RouterModule } from '@angular/router';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { APP_BASE_HREF } from '@angular/common';
import { OwlDateTimeModule, OWL_DATE_TIME_FORMATS } from 'ng-pick-datetime';
import { OwlMomentDateTimeModule } from 'ng-pick-datetime-moment';
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';

import {
  MatAutocompleteModule,
  MatButtonModule,
  MatCheckboxModule,
  MatFormFieldModule,
  MatInputModule,
  MatRadioModule,
  MatSnackBarModule,
  MatToolbarModule,
  MatCardModule,
  MatProgressSpinnerModule,
  MatProgressBarModule,
  MatIconModule,
  MatListModule,
  MatMenuModule,
  MatSelectModule,
  MatDialogModule,
  MatPaginatorModule,
  MatTooltipModule,
  MatExpansionModule,
  MatSlideToggleModule
} from '@angular/material';

import { AppComponent } from './app.component';
import { AppRoutes } from './app.routing';
import { ListViewComponent } from './components/list-view/list-view.component';
import { EditViewComponent } from './components/edit-view/edit-view.component';
import { QueryListResolve } from './resolvers/query-list.resolve.service';
import { QueryViewResolve } from './resolvers/query-view.resolve.service';
import { TimezoneSelectorComponent } from './components/timezone-selector/timezone-selector.component';
import { CronGeneratorComponent } from './components/cron-generator/cron-generator.component';
import { CanDeactivateGuard } from './services/app-deactivate-guard.service';
import { ConfirmDialogViewComponent } from './components/confirm-dialog/confirm-dialog.component';
import { RequestInterceptor } from './interceptors/http.interceptor';

export const CUSTOM_DATE_TIME_FORMATS = {
  parseInput: 'YYYY-MM-DDTHH:mm:ssZZ',
  fullPickerInput: 'YYYY-MM-DD HH:mm:ss',
  datePickerInput: 'YYYY-MM-DD',
  timePickerInput: 'THH:mm:ss',
  monthYearLabel: 'MMM YYYY',
  dateA11yLabel: 'YYYY',
  monthYearA11yLabel: 'MMM YYYY',
};

@NgModule({
  declarations: [
    AppComponent,
    ListViewComponent,
    EditViewComponent,
    TimezoneSelectorComponent,
    CronGeneratorComponent,
    ConfirmDialogViewComponent
  ],
  imports: [
    RouterModule.forRoot(AppRoutes),
    BrowserModule,
    MatAutocompleteModule,
    MatButtonModule,
    MatCheckboxModule,
    MatFormFieldModule,
    MatInputModule,
    MatRadioModule,
    MatSnackBarModule,
    MatToolbarModule,
    MatCardModule,
    MatProgressSpinnerModule,
    MatProgressBarModule,
    MatIconModule,
    MatListModule,
    MatMenuModule,
    BrowserAnimationsModule,
    MatSelectModule,
    MatDialogModule,
    FormsModule,
    ReactiveFormsModule,
    OwlDateTimeModule,
    OwlMomentDateTimeModule,
    HttpClientModule,
    MatPaginatorModule,
    MatTooltipModule,
    MatExpansionModule,
    MatSlideToggleModule
  ],
  providers: [
    {provide: APP_BASE_HREF, useValue : '/' },
    QueryListResolve,
    QueryViewResolve,
    CanDeactivateGuard,
    { provide: HTTP_INTERCEPTORS, useClass: RequestInterceptor, multi: true },
    { provide: OWL_DATE_TIME_FORMATS, useValue: CUSTOM_DATE_TIME_FORMATS }
  ],
  bootstrap: [AppComponent],
  entryComponents: [ConfirmDialogViewComponent]
})
export class AppModule { }
