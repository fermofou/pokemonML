export function getInvestmentMessage(): string {
  const messages = [
    "See Your Investment Grow",
    "Yes, Your Money Was Well Spent",
    "Watch Your Cards Appreciate",
    "Your Collection = Your Retirement Fund",
    "Totally Not an Addiction, It's Investing",
    "Better Than Stocks (Probably)",
    "Your Future Self Will Thank You",
    "Turning Cards into Cash Flow",
    "Chat you are cooked",
  ];

  const dayOfYear = Math.floor(
    (Date.now() - new Date(new Date().getFullYear(), 0, 0).getTime()) /
      (1000 * 60 * 60 * 24)
  );
  return messages[dayOfYear % messages.length];
}
