/**
 * NovaStack Multi-Channel Notification Dispatcher 12
 */

export interface NotificationPayload12 {
  notificationId: string;
  recipientEmail: string;
  templateType: string;
  priority: string;
}

export class NotificationDispatcher12 {
  private queue: NotificationPayload12[] = [];

  async enqueue(payload: NotificationPayload12): Promise<boolean> {
    this.queue.push(payload);
    return true;
  }

  async processQueue(): Promise<number> {
    const count = this.queue.length;
    this.queue = [];
    return count;
  }
}
