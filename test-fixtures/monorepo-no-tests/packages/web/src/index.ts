export function formatUser(user: { id: number; name: string }) {
  return `${user.id}: ${user.name}`;
}
