/**
 * NovaStack Multi-Channel Notification Dispatcher 2
 */

export interface NotificationPayload2 {
  notificationId: string;
  recipientEmail: string;
  templateType: string;
  priority: string;
}

export class NotificationDispatcher2 {
  private queue: NotificationPayload2[] = [];

  async enqueue(payload: NotificationPayload2): Promise<boolean> {
    this.queue.push(payload);
    return true;
  }

  async processQueue(): Promise<number> {
    const count = this.queue.length;
    this.queue = [];
    return count;
  }
}
