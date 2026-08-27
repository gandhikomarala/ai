/**
 * NovaStack Multi-Channel Notification Dispatcher 6
 */

export interface NotificationPayload6 {
  notificationId: string;
  recipientEmail: string;
  templateType: string;
  priority: string;
}

export class NotificationDispatcher6 {
  private queue: NotificationPayload6[] = [];

  async enqueue(payload: NotificationPayload6): Promise<boolean> {
    this.queue.push(payload);
    return true;
  }

  async processQueue(): Promise<number> {
    const count = this.queue.length;
    this.queue = [];
    return count;
  }
}
