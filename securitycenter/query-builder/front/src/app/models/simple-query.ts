import { LastExecution } from './last-execution';

export class SimpleQuery {
  name: string;
  description: string;
  timestamp: string;
  uuid: string;
  owner: string;
  nextRun: string;
  mark: string;
  sendNotification: boolean;
  lastExecution: LastExecution;

  constructor (name, description, timestamp, uuid, owner, nextRun, mark, sendNotification, lastExecution) {
    this.name = name;
    this.description = description;
    this.timestamp = timestamp;
    this.uuid = uuid;
    this.owner = owner;
    this.nextRun = nextRun;
    this.mark = mark;
    this.lastExecution = lastExecution;
    this.sendNotification = sendNotification;
  }
}
