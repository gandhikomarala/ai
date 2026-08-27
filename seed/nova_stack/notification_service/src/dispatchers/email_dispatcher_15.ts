/**
 * NovaStack Multi-Channel Notification Dispatcher 15
 */

export interface NotificationPayload15 {
  notificationId: string;
  recipientEmail: string;
  templateType: string;
  priority: string;
}

export class NotificationDispatcher15 {
  private queue: NotificationPayload15[] = [];

  async enqueue(payload: NotificationPayload15): Promise<boolean> {
    this.queue.push(payload);
    return true;
  }

  async processQueue(): Promise<number> {
    const count = this.queue.length;
    this.queue = [];
    return count;
  }
}
