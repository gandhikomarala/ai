/**
 * NovaStack Multi-Channel Notification Dispatcher 13
 */

export interface NotificationPayload13 {
  notificationId: string;
  recipientEmail: string;
  templateType: string;
  priority: string;
}

export class NotificationDispatcher13 {
  private queue: NotificationPayload13[] = [];

  async enqueue(payload: NotificationPayload13): Promise<boolean> {
    this.queue.push(payload);
    return true;
  }

  async processQueue(): Promise<number> {
    const count = this.queue.length;
    this.queue = [];
    return count;
  }
}
