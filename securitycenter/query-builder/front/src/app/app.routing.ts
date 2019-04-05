import { RouterModule, Routes } from '@angular/router';

import { ListViewComponent } from './components/list-view/list-view.component';
import { EditViewComponent } from './components/edit-view/edit-view.component';
import { QueryListResolve } from './resolvers/query-list.resolve.service';
import { QueryViewResolve } from './resolvers/query-view.resolve.service';
import { CanDeactivateGuard } from './services/app-deactivate-guard.service';

export const AppRoutes: Routes = [
  { path: '',  component: ListViewComponent, resolve: { data: QueryListResolve } },
  { path: 'query/:id', component: EditViewComponent, canDeactivate: [CanDeactivateGuard] , resolve: { data: QueryViewResolve } },
  { path: 'query', component: EditViewComponent, canDeactivate: [CanDeactivateGuard] },
  { path: '**', redirectTo: '', pathMatch: 'full' }
];
