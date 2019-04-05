import { Step } from './step';

export class Query {
  name: string;
  description: string;
  steps: Array<Step>;
  topic: string;
  uuid: string;
  owner: string;
  schedule: string;
  sendNotification: boolean;

  constructor (name?, desc?, steps?, topic?, uuid?, owner?, schedule?, sendNotification?) {
    this.name = name || '';
    this.description = desc || '';
    if (!steps) {
      steps = [];
    }
    this.steps = steps;
    this.topic = topic || '';
    this.uuid = uuid;
    this.owner = owner;
    this.schedule = schedule || '';
    this.sendNotification = sendNotification || false;
  }

  public addStep(step: Step) {
    if (!this.steps) {
      this.steps = [];
    }
    this.steps.push(step);
  }

  public modifyFirstStepJoins(inJoin, outJoin) {
    this.steps[0].setJoins(inJoin, outJoin);
  }

  public toPayload(ignoreSchedule: boolean) {
    if (ignoreSchedule) {
      this.schedule = null;
    }
    const isSingleStep = this.steps.length === 1;
    this.steps.forEach((step, i) => {
      step.toPayload(isSingleStep, i === this.steps.length - 1);
    });
  }

  public deleteStep(stepIndex) {
    if (this.steps[stepIndex - 1]) {
      this.steps[stepIndex - 1].clearOutJoin();
    }
    if (this.steps[stepIndex + 1]) {
      this.steps[stepIndex + 1].clearInJoin();
    }
    this.steps.splice(stepIndex, 1);
  }

}
