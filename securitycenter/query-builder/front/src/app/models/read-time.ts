import * as moment from 'moment-timezone';

export class ReadTime {
  type: string;
  value: string;
  timeZone: string;
  momentValue: moment.Moment;
  invalidValue: string;

  constructor (type?, value?, timeZone?, momentValue?) {
    this.type = type || 'TIMESTAMP';
    this.value = value || '';
    this.timeZone = timeZone || '';
    this.momentValue = momentValue;
    this.invalidValue = null;
  }

  public toPayload() {
    if (this.type === 'TIMESTAMP') {
      this.value = '';
      if (this.momentValue) {
        this.value = this.momentValue.format('YYYY-MM-DDTHH:mm:ssZZ');
      } else {
        this.value = this.invalidValue;
      }
      if (!this.timeZone) {
        this.timeZone = moment.tz.guess();
      }
    } else {
      delete this.momentValue;
      delete this.timeZone;
    }
  }

  public fillMomentTime() {
    if (this.type === 'TIMESTAMP' && this.value) {
      const dateValue = this.value.substr(0, 19);
      this.value = dateValue;
      this.momentValue = moment(dateValue);
    }
  }

  public updateDate(invalidValue) {
    if (this.timeZone && !invalidValue) {
      this.momentValue = moment.tz(this.momentValue.format('YYYY-MM-DDTHH:mm:ss'), this.timeZone);
    }
    this.invalidValue = invalidValue;
  }

  public updateTimezone() {
    this.timeZone = this.timeZone || moment.tz.guess();
    if (this.momentValue) {
      this.momentValue = moment(this.momentValue).tz(this.timeZone);
    }
  }
}
