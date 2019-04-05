import { AppPage } from './app.po';

describe('workspace-project App', () => {
  let page: AppPage;

  beforeEach(() => {
    page = new AppPage();
  });

  it('should display Application Title', () => {
    page.navigateTo();
    expect(page.getAppTitle()).toEqual('Query list');
  });
});
