/*
 * hostapd / KARMA attack victim table
 *
 *
 */

// define under the karma attack compiler flag is on
#ifdef CONFIG_KARMA_ATTACK
#include "utils/includes.h"
#include "utils/common.h"
#include "utils/eloop.h"
#include "ap_config.h"
#include "hostapd.h"
#include "sta_info.h"

void free_sta_karma_data(struct hostapd_data *hapd,
        struct hostapd_karma_data * karma_data)
{
    os_free(karma_data); 
}

void free_all_karma_data(struct hostapd_data *hapd)
{
    struct hostapd_karma_data* karma_data, *prev;

    karma_data = hapd->karma_data_list;

    while (karma_data) {
        prev = karma_data;
        karma_data = karma_data->next;
		wpa_printf(MSG_INFO, "Removing karma station " MACSTR,
			   MAC2STR(prev->mac_addr));
        free_sta_karma_data(hapd, prev);
    }
}

struct hostapd_karma_data * get_sta_karma_data(struct hostapd_data *hapd, const u8 *mac_addr)
{
	struct hostapd_karma_data *s = hapd->karma_data_list;
    
	while (s != NULL && os_memcmp(s->mac_addr, mac_addr, 6) != 0)
		s = s->next;
	return s;
}

// add karma data to head
void add_sta_karma_data(struct hostapd_data *hapd,
        struct hostapd_karma_data *data)
{
    data->next = hapd->karma_data_list;
    hapd->karma_data_list = data;
}

// create karma data
struct hostapd_karma_data* create_karma_data(const u8 *ssid, const u8 *mac_addr,
        size_t ssid_len)
{
    struct hostapd_karma_data *karma_data = os_malloc(sizeof(struct hostapd_karma_data));
    os_memcpy(karma_data->ssid, ssid, ssid_len);
    os_memcpy(karma_data->mac_addr, mac_addr, 6);
    karma_data->ssid_len = ssid_len;
    return karma_data;
}

// ctype binders for get essid/mac addresses to the Python wrapper
struct hostapd_karma_data * get_assoc_karma_data(void)
{
    extern struct hostapd_data *g_hapd_data;
    struct hostapd_karma_data *s = g_hapd_data->karma_data_list;
    struct sta_info *sta = NULL;
    // clear all the assoc bit since the sta may be disconnected now
	while (s != NULL) {
        s->is_assoc = 0;
		s = s->next;
    }
    s = g_hapd_data->karma_data_list;
    // set the assoc bit
    while (s != NULL) {
        sta = ap_get_sta(g_hapd_data, s->mac_addr);
        if (sta != NULL && (sta->flags & WLAN_STA_ASSOC)) {
            s->is_assoc = 1; 
        }
        s = s->next;
    }
    // return the head which is truely associated
    return g_hapd_data->karma_data_list;
}
#endif
