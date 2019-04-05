import { Component, Inject } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material';

@Component({
  selector: 'qb-confirm-dialog-view',
  templateUrl: './confirm-dialog.component.html',
  styleUrls: ['./confirm-dialog.component.scss']
})
export class ConfirmDialogViewComponent {
  constructor(
    public dialogRef: MatDialogRef<ConfirmDialogViewComponent>,
    @Inject(MAT_DIALOG_DATA) public data: any) { }

  onCancel(): void {
    this.data.isConfirmed = false;
    this.dialogRef.close(false);
  }

  onConfirm(): void {
    this.data.isConfirmed = true;
    this.dialogRef.close(true);
  }

}
