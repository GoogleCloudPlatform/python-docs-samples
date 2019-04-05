import { TestBed, inject } from '@angular/core/testing';

import { AppService } from './app.service';

describe('AppServiceService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [AppService]
    });
  });

  it('creates the AppService', inject([AppService], (service: AppService) => {
    expect(service).toBeTruthy();
  }));

  it('sets toolbar title correctly', inject([AppService], (service: AppService) => {
    service.setToolbarInfo({title: 'Any', route: 'any/route'});
    expect({title: 'Any', route: 'any/route'}).toEqual(service.getToolbarInfo());
  }));
});
