import { Component, OnInit, ViewChild, ElementRef } from '@angular/core';
import { QueryService } from '../services/query.service';
import { MatSnackBar} from '@angular/material';
import { Injectable } from '@angular/core';

@Injectable({
    providedIn: 'root'
  })
export class SessionErrorHandler {
    iapSessionRefreshWindow: any;
    genericErrorMessage = 'Some error ocurred, please try again or contact support.';

    constructor(private queryService: QueryService, public snackBar: MatSnackBar) {
        this.iapSessionRefreshWindow = null;
    }

    private checkIfSessionIsExpired(err) {
        return err.message === 'Session Expired';
    }

    public handleExpiredSession(err, run_query = false) {
        if (this.checkIfSessionIsExpired(err)) {
            const snackRef = this.snackBar.open('Your session has expired! Please refresh your session.', 'OK', { duration: 5000 });
            snackRef.afterDismissed().subscribe(() => {
            this.sessionRefreshClicked();
            });
        } else if (!run_query) {
            this.snackBar.open(this.genericErrorMessage, 'OK', { duration: 2000 });
        }
    }

    private sessionRefreshClicked() {
        const self = this;
        const checkSessionRefresh = function() {
            if (self.iapSessionRefreshWindow != null && !self.iapSessionRefreshWindow.closed) {
                self.queryService.getQueryList(1, 2, this.textSearchControl.value).then(function(response) {
                self.iapSessionRefreshWindow.close();
                self.iapSessionRefreshWindow = null;
                }).catch (function(err) {
                    if (self.checkIfSessionIsExpired(err)) {
                        self.iapSessionRefreshWindow.close();
                        self.iapSessionRefreshWindow = null;
                        location.reload();
                    }
                });
            }
        };

        if (this.iapSessionRefreshWindow == null) {
            this.iapSessionRefreshWindow = window.open('/_gcp_iap/do_session_refresh', '_blank');
            window.setTimeout(checkSessionRefresh, 700);
        }
        return false;
    }
}
