import { ReadTime } from './read-time';
import { Threshold } from './threshold';

export class Step {
  order: Number;
  kind: string;
  readTime: ReadTime;
  filter: string;
  inJoin: string;
  outJoin: string;
  compareDuration: string;
  threshold: Threshold;

  constructor(order?, kind?, readTime?, filter?, inJoin?, outJoin?, compareDuration?, threshold?) {
    this.order = order;
    this.kind = kind || 'ASSET';
    if (!readTime) {
      readTime = new ReadTime(null, null, null, null);
    }
    this.readTime = readTime;
    this.filter = filter || '';
    this.inJoin = inJoin || '';
    this.outJoin = outJoin || '';
    this.compareDuration = compareDuration || '';
    if (!threshold) {
      threshold = new Threshold(null, null);
    }
    this.threshold = threshold;
  }

  public setJoins(inJoin, outJoin) {
    this.inJoin = inJoin;
    this.outJoin = outJoin;
  }

  public toPayload(isSingleStep, isLastStep) {
    if (this.kind !== 'ASSET') {
      delete this.compareDuration;
    }
    if (isSingleStep) {
      this.clearInJoin();
      this.clearOutJoin();
    } else if (isLastStep) {
      this.clearOutJoin();
    }
    this.readTime.toPayload();
  }

  public clearOutJoin() {
    delete this.outJoin;
  }

  public clearInJoin() {
    delete this.inJoin;
  }

  public verifyJoins(joinType): boolean {
    if (joinType === 'inJoin') {
      return !!(this.inJoin);
    }
    if (joinType === 'outJoin') {
      return !!(this.outJoin);
    }
  }
}
