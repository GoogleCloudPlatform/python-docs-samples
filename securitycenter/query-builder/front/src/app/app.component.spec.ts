import { TestBed, async } from '@angular/core/testing';
import { AppComponent } from './app.component';
import { ListViewComponent } from './components/list-view/list-view.component';
import { EditViewComponent } from './components/edit-view/edit-view.component';
import { CronGeneratorComponent } from './components/cron-generator/cron-generator.component';
import { RouterModule } from '@angular/router';
import { AppRoutes } from './app.routing';
import {APP_BASE_HREF} from '@angular/common';

import {
  MatToolbarModule,
  MatCardModule,
  MatIconModule,
  MatListModule,
  MatMenuModule,
  MatFormFieldModule,
  MatSelectModule,
  MatPaginatorModule,
  MatAutocompleteModule,
  MatTooltipModule,
  MatCheckboxModule,
  MatSlideToggleModule
} from '@angular/material';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { OwlDateTimeModule } from 'ng-pick-datetime';
import { TimezoneSelectorComponent } from './components/timezone-selector/timezone-selector.component';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatExpansionModule } from '@angular/material/expansion';


describe('AppComponent', () => {
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
        RouterModule,
        RouterModule.forRoot(AppRoutes),
        FormsModule,
        ReactiveFormsModule,
        MatPaginatorModule,
        MatAutocompleteModule,
        OwlDateTimeModule,
        MatProgressSpinnerModule,
        MatExpansionModule,
        MatTooltipModule,
        MatCheckboxModule,
        MatSlideToggleModule
      ],
      declarations: [
        AppComponent,
        ListViewComponent,
        EditViewComponent,
        TimezoneSelectorComponent,
        CronGeneratorComponent
      ],
      providers: [{provide: APP_BASE_HREF, useValue : '/' }]
    }).compileComponents();
  }));
  it('creates the app', async(() => {
    const fixture = TestBed.createComponent(AppComponent);
    const app = fixture.debugElement.componentInstance;
    expect(app).toBeTruthy();
  }));
});
