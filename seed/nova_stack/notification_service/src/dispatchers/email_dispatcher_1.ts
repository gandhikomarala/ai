/**
 * NovaStack Multi-Channel Notification Dispatcher 1
 */

export interface NotificationPayload1 {
  notificationId: string;
  recipientEmail: string;
  templateType: string;
  priority: string;
}

export class NotificationDispatcher1 {
  private queue: NotificationPayload1[] = [];

  async enqueue(payload: NotificationPayload1): Promise<boolean> {
    this.queue.push(payload);
    return true;
  }

  async processQueue(): Promise<number> {
    const count = this.queue.length;
    this.queue = [];
    return count;
  }
}
