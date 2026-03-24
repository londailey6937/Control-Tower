// ============================================================
// SUPABASE CLIENT — Realtime Message Board Backend
// ============================================================

import {
  createClient,
  type SupabaseClient,
  type RealtimeChannel,
} from "@supabase/supabase-js";

const SUPABASE_URL = "https://fllqdhvvnqoayugohzld.supabase.co";
const SUPABASE_ANON_KEY = "sb_publishable_mM9VIE_SOUb956b_7UeTzw_n9QaNuiL";

export const supabase: SupabaseClient = createClient(
  SUPABASE_URL,
  SUPABASE_ANON_KEY,
);

// ── Types matching the DB schema ──────────────────
export interface DbMessage {
  id: string;
  q_num: number;
  sender: "pmp" | "inventor";
  text: string;
  created_at: string;
  read_by: string[];
}

// ── Online detection ───────────────────────────────
let _online = navigator.onLine;
window.addEventListener("online", () => {
  _online = true;
});
window.addEventListener("offline", () => {
  _online = false;
});
export function isOnline(): boolean {
  return _online;
}

// ── Message CRUD ───────────────────────────────────

export async function fetchMessages(): Promise<DbMessage[]> {
  const { data, error } = await supabase
    .from("messages")
    .select("*")
    .order("created_at", { ascending: true });
  if (error) {
    console.error("Supabase fetchMessages:", error);
    return [];
  }
  return data ?? [];
}

export async function fetchMessagesByQuestion(
  qNum: number,
): Promise<DbMessage[]> {
  const { data, error } = await supabase
    .from("messages")
    .select("*")
    .eq("q_num", qNum)
    .order("created_at", { ascending: true });
  if (error) {
    console.error("Supabase fetchByQ:", error);
    return [];
  }
  return data ?? [];
}

export async function insertMessage(
  msg: Omit<DbMessage, "id" | "created_at">,
): Promise<DbMessage | null> {
  const { data, error } = await supabase
    .from("messages")
    .insert(msg)
    .select()
    .single();
  if (error) {
    console.error("Supabase insertMessage:", error);
    return null;
  }
  return data;
}

export async function markMessageRead(
  msgId: string,
  role: string,
): Promise<void> {
  // Use Postgres array_append to atomically add the role
  const { error } = await supabase.rpc("mark_read", {
    msg_id: msgId,
    reader: role,
  });
  if (error) console.error("Supabase markRead:", error);
}

export async function deleteMessages(qNum: number): Promise<boolean> {
  const { error } = await supabase.from("messages").delete().eq("q_num", qNum);
  if (error) {
    console.error("Supabase deleteMessages:", error);
    return false;
  }
  return true;
}

// ── Realtime Subscription ──────────────────────────

let _channel: RealtimeChannel | null = null;
type MessageCallback = (msg: DbMessage) => void;

export function subscribeMessages(
  onInsert: MessageCallback,
  onUpdate?: MessageCallback,
): void {
  if (_channel) _channel.unsubscribe();

  _channel = supabase
    .channel("messages-realtime")
    .on(
      "postgres_changes",
      { event: "INSERT", schema: "public", table: "messages" },
      (payload) => onInsert(payload.new as DbMessage),
    )
    .on(
      "postgres_changes",
      { event: "UPDATE", schema: "public", table: "messages" },
      (payload) => {
        if (onUpdate) onUpdate(payload.new as DbMessage);
      },
    )
    .subscribe();
}

export function unsubscribeMessages(): void {
  if (_channel) {
    _channel.unsubscribe();
    _channel = null;
  }
}
