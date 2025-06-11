import dropbox,os
from dropbox.exceptions import ApiError
from dropbox.files import WriteMode

DROPBOX_ACCESS_TOKEN = "sl.u.AFx9LKG8Rsd3lUOClMGGPP1er1TVrSUvkkuV3KZ3DWbtGMvRLK0uIggnRbc5tM9YWKJ-0vG83aTZs8aJM9LYZvF37ZIcJ-_w8OFV7Hu4dLSuiEpwBMpVj0gISzGj6u1cV4TL1P3Cfk_jO8dwMKluhJxDk2IuVlfj8q3PtPqOnR5Q7FcaDH9WpHpzmPRTeSil0fxOuHvJc7aY-kemK64xeQfEwWXPF9nIJIBEi2yfoOur50QSbSryUwwWmh0BdvgdZmfkfkIiPnT4BiXhmF5UrR1T9UUnG3E1ECt44p79sRZFeBH16AOWFIEPs1kD188TqnDVZcxoe9_vd8AZfCj_SH7kEeefpG_aopudBWR9b_sjXPv6XToVlgKQ3lu_7WXKTvAcaGuqFoUBSrv4e5_4HT-JaA1RVy3pSphhcgYn2LDGgRuXdeXVBOrI6jcn2qhwW5egL629edaYawtNfWc7tt89nGscxmx2JJaEwda-cnm3bGpjlN9Sqmnm68LvnhoxDecLeHjTrU47ukxttIh8yr7S7SpFvMnPPLDqo-4lCa7aGWnCFL2ur9oZqq_QaMqvQ-v8c5IuYTAmaSkTXA7l7LWDBE0V6mi57x9riWPVa3fwKjRY1VT_oIjeeSsKWcOq6IxxUNIEHcBLrAz5_Bsf4S8Kkd1lagDvk-C5Z2ZJJ3bMfNuqrfEvtEH9w3Ru-NwsUgoTDbJPQfidvCVAo-gpHp9TU-dTc0G5IAsJFbmZO5dF9a_TEoubrQrSVRnkBmMs9dPKPflhklouBfl0dDnQfRaUC1dQ4BQgCXpnbn3CdkM4CjPZtxMKzmDJA0mksnHuMaBVAeOmxqQBPEcS7ORPnbK7GclkHfil95RVlF4tLdIEsWGtOn95-zpqlHW-f5eAjF7TqsSqFQ9fEWDrnOIgZOGt1Cn9eUtpl8X3xNfPur_D7TW4xhYmg9onwRlV62vXzDYhPRZpwN2Kpgd2oU1O3Ywl2FllZERVY5cv_pq9C2PfOWybeHTJmNfF3vPxHqsWKk-3Ivo69NMCmS-wCEko1cnSktRkx52TrzjpaDbOW7456QfpNa7q2g3Md-GuhrXVoLtiW5d7dISf47Skd1MtkWq659CAe2wUIu8_7WhTkMhdBRZ27kGbI1_yb_Yjq4KHY4Hb_eW1iD-oS0QkAe_3XkuBYOXoJ_ei4z4rN-Dlns6f4rKPdjcjKH7fTDF3b4f6bZb-59NXa6RPbZ1KsXJCISGB11FbaBERpM6n8_mZtwQsawtuxeIAvwSssazvXLFzj9II2Xe9UkmIb3Y5Mv8Bau2zSUT29_I_Gpm2v5EmdqNESj8eLGCdaAk8zgT5mOG6xSsFWInRZq_PK1rDNjfTi34sLdxBQdKG6QASzi6km29kH4BhurOxNYtQBmNlCGM_EOvQaD5Cj2ATH23zKqGyA64TfL2mklBcWKsT8f-7znBCgA"

def upload_to_dropbox(file_path):
    try:
        dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)
        dropbox_path = f"/{os.path.basename(file_path)}"

        with open(file_path, "rb") as f:
            dbx.files_upload(f.read(), dropbox_path, mode=dropbox.files.WriteMode.overwrite)

        try:
            shared_link_metadata = dbx.sharing_create_shared_link_with_settings(dropbox_path)
        except ApiError as e:
            if e.error.is_shared_link_already_exists():
                links = dbx.sharing_list_shared_links(path=dropbox_path).links
                if links:
                    shared_link_metadata = links[0]
                else:
                    return "Error: Could not retrieve existing shared link.", None
            else:
                return f"Error uploading: {e}", None

        return shared_link_metadata.url, dropbox_path 

    except Exception as e:
        return f"Error uploading: {e}", None