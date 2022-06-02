def channel_link_to_id(link: str):
    return link.split("/channels/")[1].split("/")[0]