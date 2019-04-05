export class LastExecution {
  date: string;
  result: number;
  status: string;

  constructor(date?, result?, status?) {
    this.date = date || '';
    this.result = result || 0;
    this.status = status || 'NOT_EXECUTED';
  }
}
