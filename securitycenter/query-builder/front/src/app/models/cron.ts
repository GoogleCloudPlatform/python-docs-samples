export class Cron {
  minute: number;
  hour: number;
  dayOfMonth: number;
  month: number;
  dayOfWeek: Array<number>;

  constructor (kind: string) {
    switch (kind.toUpperCase()) {
      case 'HOUR':
        this.minute = 0;
        this.hour = 1;
        this.dayOfMonth = null;
        this.month = null;
        this.dayOfWeek = null;
        break;
      case 'DAY':
        this.minute = 0;
        this.hour = 0;
        this.dayOfMonth = 1;
        this.month = null;
        this.dayOfWeek = null;
        break;
      case 'WEEK':
        this.minute = 0;
        this.hour = 0;
        this.dayOfMonth = null;
        this.month = null;
        this.dayOfWeek = [0];
        break;
      default:
        this.minute = null;
        this.hour = null;
        this.dayOfMonth = null;
        this.month = null;
        this.dayOfWeek = null;
        break;
    }
  }

  generateExpression(kind) {
    const cronArray = [
      this.minute === null ? '*' : this.minute,
      this.hour === null ? '*' : kind.hourPrefix + this.hour,
      this.dayOfMonth === null ? '*' : kind.dayPrefix + this.dayOfMonth,
      this.month === null ? '*' : '',
      this.dayOfWeek === null ? '*' : this.dayOfWeek.join(',')
    ];
    return cronArray.join(' ');
  }

  buildFromExpression(cronExp) {
    const cronArray = cronExp.split(' ');
    this.minute = cronArray[0] === '*' ? null : this.getValue(cronArray[0]);
    this.hour = cronArray[1] === '*' ? null : this.getValue(cronArray[1]);
    this.dayOfMonth = cronArray[2] === '*' ? null : this.getValue(cronArray[2]);
    this.month = null;
    if (cronArray[4] !== '*') {
      this.dayOfWeek = [];
      const days = cronArray[4].split(',');
      days.forEach(dayValue => {
        this.dayOfWeek.push(this.getValue(dayValue));
      });
    }
  }

  private getValue(stringValue: string): number {
    const value = stringValue.replace('*/', '');
    return Number(value);
  }
}
