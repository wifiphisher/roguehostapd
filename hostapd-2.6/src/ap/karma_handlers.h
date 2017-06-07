#ifndef KARMA_HANDLERS_H
#define KARMA_HANDLERS_H
extern void free_sta_karma_data(struct hostapd_data *hapd, struct hostapd_karma_data *);
extern struct hostapd_karma_data *get_sta_karma_data(
                    struct hostapd_data *hapd, const u8 *mac_addr);
extern struct hostapd_karma_data* create_karma_data(
                    const u8 *ssid, const u8 *mac_addr, size_t ssid_len);
extern void add_sta_karma_data(
                    struct hostapd_data *hapd, struct hostapd_karma_data *data);
extern void free_all_karma_data(struct hostapd_data *hapd);
extern struct hostapd_karma_data *get_assoc_karma_data(void);
#endif
