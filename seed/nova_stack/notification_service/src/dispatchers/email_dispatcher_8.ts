/**
 * NovaStack Multi-Channel Notification Dispatcher 8
 */

export interface NotificationPayload8 {
  notificationId: string;
  recipientEmail: string;
  templateType: string;
  priority: string;
}

export class NotificationDispatcher8 {
  private queue: NotificationPayload8[] = [];

  async enqueue(payload: NotificationPayload8): Promise<boolean> {
    this.queue.push(payload);
    return true;
  }

  async processQueue(): Promise<number> {
    const count = this.queue.length;
    this.queue = [];
    return count;
  }
}
