/**
 * NovaStack Multi-Channel Notification Dispatcher 20
 */

export interface NotificationPayload20 {
  notificationId: string;
  recipientEmail: string;
  templateType: string;
  priority: string;
}

export class NotificationDispatcher20 {
  private queue: NotificationPayload20[] = [];

  async enqueue(payload: NotificationPayload20): Promise<boolean> {
    this.queue.push(payload);
    return true;
  }

  async processQueue(): Promise<number> {
    const count = this.queue.length;
    this.queue = [];
    return count;
  }
}
