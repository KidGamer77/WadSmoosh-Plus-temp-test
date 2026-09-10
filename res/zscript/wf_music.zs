//-----------------------------------------------------------------------------
// UZDoom 5.x music swapper
// PostUiTick is UI — helpers used there must be ui or clearscope.
// Never call S_ChangeMusic unless the track actually changed.
//-----------------------------------------------------------------------------

class WadFusionMusicHandler : StaticEventHandler
{
    clearscope bool CVBool(Name n)
    {
        let cv = CVar.FindCVar(n);
        return cv != null && cv.GetBool();
    }

    ui string CurrentTrack()
    {
        string track = MusPlaying.Name;
        track.ToLower();
        return track;
    }

    ui void PlayIfChanged(string track)
    {
        string current = CurrentTrack();
        if (track.Length() == 0 || track == current)
            return;
        S_ChangeMusic(track);
    }

    clearscope string MidiForHulshultOr3DO(string track, string mapName)
    {
        if (track == "3_e1m1" || track == "h_e1m1") return "d_e1m1";
        if (track == "3_e1m2" || track == "h_e1m2") return "d_e1m2";
        if (track == "3_e1m3" || track == "h_e1m3") return "d_e1m3";
        if (track == "3_e1m4" || track == "h_e1m4") return "d_e1m4";
        if (track == "3_e1m5" || track == "h_e1m5") return "d_e1m5";
        if (track == "3_e1m6" || track == "h_e1m6")
            return (mapName == "e3m6") ? "d_e3m6" : "d_e1m6";
        if (track == "3_e1m7" || track == "h_e1m7")
        {
            if (mapName == "e2m5" || mapName == "e4m8") return "d_e2m5";
            if (mapName == "e3m5") return "d_e3m5";
            return "d_e1m7";
        }
        if (track == "3_e1m8" || track == "h_e1m8")
            return (mapName == "e3m4") ? "d_e3m4" : "d_e1m8";
        if (track == "3_e1m9" || track == "h_e1m9")
            return (mapName == "e3m9") ? "d_e3m9" : "d_e1m9";
        if (track == "3_e2m1" || track == "h_e2m1") return "d_e2m1";
        if (track == "3_e2m2" || track == "h_e2m2") return "d_e2m2";
        if (track == "3_e2m3" || track == "h_e2m3") return "d_e2m3";
        if (track == "3_e2m4" || track == "h_e2m4") return "d_e2m4";
        if (track == "3_e2m5" || track == "h_e2m5") return "d_e2m5";
        if (track == "3_e2m6" || track == "h_e2m6") return "d_e2m6";
        if (track == "3_e2m7" || track == "h_e2m7")
            return (mapName == "e3m7") ? "d_e3m7" : "d_e2m7";
        if (track == "3_e2m8" || track == "h_e2m8") return "d_e2m8";
        if (track == "3_e2m9" || track == "h_e2m9")
            return (mapName == "e3m1") ? "d_e3m1" : "d_e2m9";
        if (track == "3_e3m1") return "d_e3m1";
        if (track == "3_e3m2" || track == "h_e3m2") return "d_e3m2";
        if (track == "3_e3m3" || track == "h_e3m3") return "d_e3m3";
        if (track == "3_e3m4") return "d_e3m4";
        if (track == "3_e3m5") return "d_e3m5";
        if (track == "3_e3m6") return "d_e3m6";
        if (track == "3_e3m7") return "d_e3m7";
        if (track == "3_e3m8" || track == "h_e3m8") return "d_e3m8";
        if (track == "3_e3m9") return "d_e3m9";
        if (track == "3_inter") return "d_inter";
        if (track == "3_intro" || track == "h_intro") return "d_intro";
        if (track == "3_victor" || track == "h_victor") return "d_victor";
        if (track == "3_bunny" || track == "h_bunny") return "d_bunny";
        if (track == "h_adrian") return "d_adrian";
        if (track == "h_ampie") return "d_ampie";
        if (track == "h_betwee") return "d_betwee";
        if (track == "h_countd")
            return (mapName == "map21") ? "d_count2" : "d_countd";
        if (track == "h_ddtblu")
        {
            if (mapName == "map22") return "d_ddtbl3";
            if (mapName == "map14") return "d_ddtbl2";
            return "d_ddtblu";
        }
        if (track == "h_dead")
            return (mapName == "map16") ? "d_dead2" : "d_dead";
        if (track == "h_doom")
            return (mapName == "map13") ? "d_doom2" : "d_doom";
        if (track == "h_evil") return "d_evil";
        if (track == "h_in_cit") return "d_in_cit";
        if (track == "h_messag")
            return (mapName == "map31") ? "d_messg2" : "d_messag";
        if (track == "h_openin") return "d_openin";
        if (track == "h_romero")
            return (mapName == "map32") ? "d_romer2" : "d_romero";
        if (track == "h_runnin")
            return (mapName == "map30") ? "d_runni2" : "d_runnin";
        if (track == "h_shawn")
        {
            if (mapName == "map29") return "d_shawn3";
            if (mapName == "map12") return "d_shawn2";
            return "d_shawn";
        }
        if (track == "h_stalks")
        {
            if (mapName == "map27") return "d_stlks3";
            if (mapName == "map11") return "d_stlks2";
            return "d_stalks";
        }
        if (track == "h_tense") return "d_tense";
        if (track == "h_the_da")
        {
            if (mapName == "map26") return "d_theda3";
            if (mapName == "map09") return "d_theda2";
            return "d_the_da";
        }
        if (track == "h_ultima") return "d_ultima";
        if (track == "h_dm2ttl") return "d_dm2ttl";
        if (track == "h_dm2int") return "d_dm2int";
        if (track == "h_read_m") return "d_read_m";
        return track;
    }

    override void WorldLoaded(WorldEvent e)
    {
        string mapName = level.MapName.MakeLower();
        string mapMusic = "d_"..mapName;
        string mapMusicShreds = mapMusic.."a";

        if (mapName.Left(3) == "e5m")
        {
            if (CVBool("wf_sigil_shreds"))
                S_ChangeMusic(mapMusicShreds);
            else
                S_ChangeMusic(mapMusic);
        }
        else if (mapName.Left(3) == "e6m")
        {
            if (CVBool("wf_sigil2_shreds"))
                S_ChangeMusic(mapMusicShreds);
            else
                S_ChangeMusic(mapMusic);
        }
    }

    override void WorldUnloaded(WorldEvent e)
    {
        string mapName = level.MapName.MakeLower();

        if (mapName.Left(3) == "e5m")
        {
            if (CVBool("wf_sigil_shreds"))
                S_ChangeMusic("s_intera");
            else
                S_ChangeMusic("s_inter");
        }
        else if (mapName.Left(3) == "e6m")
        {
            if (CVBool("wf_sigil2_shreds"))
                S_ChangeMusic("s2_intea");
            else
                S_ChangeMusic("s2_inter");
        }
    }

    override void PostUiTick()
    {
        string track = CurrentTrack();
        if (track.Length() == 0)
            return;

        string mapName = level.MapName.MakeLower();
        bool sigilOn = CVBool("wf_sigil_shreds");
        bool sigil2On = CVBool("wf_sigil2_shreds");
        bool idkfaOn = CVBool("wf_hulshult_idkfa");
        bool threeDoOn = CVBool("wf_doom3do");

        if (sigilOn)
        {
            if (track == "d_e5m1") track = "d_e5m1a";
            else if (track == "d_e5m2") track = "d_e5m2a";
            else if (track == "d_e5m3") track = "d_e5m3a";
            else if (track == "d_e5m4") track = "d_e5m4a";
            else if (track == "d_e5m5") track = "d_e5m5a";
            else if (track == "d_e5m6") track = "d_e5m6a";
            else if (track == "d_e5m7") track = "d_e5m7a";
            else if (track == "d_e5m8") track = "d_e5m8a";
            else if (track == "d_e5m9") track = "d_e5m9a";
            else if (track == "s_intro") track = "s_introa";
            else if (track == "s_inter") track = "s_intera";
        }
        else
        {
            if (track == "d_e5m1a") track = "d_e5m1";
            else if (track == "d_e5m2a") track = "d_e5m2";
            else if (track == "d_e5m3a") track = "d_e5m3";
            else if (track == "d_e5m4a") track = "d_e5m4";
            else if (track == "d_e5m5a") track = "d_e5m5";
            else if (track == "d_e5m6a") track = "d_e5m6";
            else if (track == "d_e5m7a") track = "d_e5m7";
            else if (track == "d_e5m8a") track = "d_e5m8";
            else if (track == "d_e5m9a") track = "d_e5m9";
            else if (track == "s_introa") track = "s_intro";
            else if (track == "s_intera") track = "s_inter";
        }

        if (sigil2On)
        {
            if (track == "d_e6m1") track = "d_e6m1a";
            else if (track == "d_e6m2") track = "d_e6m2a";
            else if (track == "d_e6m3") track = "d_e6m3a";
            else if (track == "d_e6m4") track = "d_e6m4a";
            else if (track == "d_e6m5") track = "d_e6m5a";
            else if (track == "d_e6m6") track = "d_e6m6a";
            else if (track == "d_e6m7") track = "d_e6m7a";
            else if (track == "d_e6m8") track = "d_e6m8a";
            else if (track == "d_e6m9") track = "d_e6m9a";
            else if (track == "s2_intro") track = "s2_intra";
            else if (track == "s2_inter") track = "s2_intea";
        }
        else
        {
            if (track == "d_e6m1a") track = "d_e6m1";
            else if (track == "d_e6m2a") track = "d_e6m2";
            else if (track == "d_e6m3a") track = "d_e6m3";
            else if (track == "d_e6m4a") track = "d_e6m4";
            else if (track == "d_e6m5a") track = "d_e6m5";
            else if (track == "d_e6m6a") track = "d_e6m6";
            else if (track == "d_e6m7a") track = "d_e6m7";
            else if (track == "d_e6m8a") track = "d_e6m8";
            else if (track == "d_e6m9a") track = "d_e6m9";
            else if (track == "s2_intra") track = "s2_intro";
            else if (track == "s2_intea") track = "s2_inter";
        }

        if (idkfaOn)
        {
            if (track == "d_e1m1" || track == "3_e1m1") track = "h_e1m1";
            else if (track == "d_e1m2" || track == "3_e1m2") track = "h_e1m2";
            else if (track == "d_e1m3" || track == "3_e1m3") track = "h_e1m3";
            else if (track == "d_e1m4" || track == "3_e1m4") track = "h_e1m4";
            else if (track == "d_e1m5" || track == "3_e1m5") track = "h_e1m5";
            else if (track == "d_e1m6" || track == "d_e3m6" || track == "3_e1m6" || track == "3_e3m6") track = "h_e1m6";
            else if (track == "d_e1m7" || track == "d_e2m5" || track == "d_e3m5" || track == "3_e1m7" || track == "3_e2m5" || track == "3_e3m5") track = "h_e1m7";
            else if (track == "d_e1m8" || track == "d_e3m4" || track == "3_e1m8" || track == "3_e3m4") track = "h_e1m8";
            else if (track == "d_e1m9" || track == "d_e3m9" || track == "3_e1m9" || track == "3_e3m9") track = "h_e1m9";
            else if (track == "d_e2m1" || track == "3_e2m1") track = "h_e2m1";
            else if (track == "d_e2m2" || track == "3_e2m2") track = "h_e2m2";
            else if (track == "d_e2m3" || track == "d_inter" || track == "3_e2m3" || track == "3_inter") track = "h_e2m3";
            else if (track == "d_e2m4" || track == "3_e2m4") track = "h_e2m4";
            else if (track == "d_e2m6" || track == "3_e2m6") track = "h_e2m6";
            else if (track == "d_e2m7" || track == "d_e3m7" || track == "3_e2m7" || track == "3_e3m7") track = "h_e2m7";
            else if (track == "d_e2m8" || track == "3_e2m8") track = "h_e2m8";
            else if (track == "d_e2m9" || track == "d_e3m1" || track == "3_e2m9" || track == "3_e3m1") track = "h_e2m9";
            else if (track == "d_e3m2" || track == "3_e3m2") track = "h_e3m2";
            else if (track == "d_e3m3" || track == "3_e3m3") track = "h_e3m3";
            else if (track == "d_e3m8" || track == "3_e3m8") track = "h_e3m8";
            else if (track == "d_intro" || track == "d_introa" || track == "3_intro") track = "h_intro";
            else if (track == "d_victor" || track == "3_victor") track = "h_victor";
            else if (track == "d_bunny" || track == "3_bunny") track = "h_bunny";
            else if (track == "d_adrian") track = "h_adrian";
            else if (track == "d_ampie") track = "h_ampie";
            else if (track == "d_betwee") track = "h_betwee";
            else if (track == "d_countd" || track == "d_count2") track = "h_countd";
            else if (track == "d_ddtblu" || track == "d_ddtbl2" || track == "d_ddtbl3") track = "h_ddtblu";
            else if (track == "d_dead" || track == "d_dead2") track = "h_dead";
            else if (track == "d_doom" || track == "d_doom2") track = "h_doom";
            else if (track == "d_evil") track = "h_evil";
            else if (track == "d_in_cit") track = "h_in_cit";
            else if (track == "d_messag" || track == "d_messg2") track = "h_messag";
            else if (track == "d_openin") track = "h_openin";
            else if (track == "d_romero" || track == "d_romer2") track = "h_romero";
            else if (track == "d_runnin" || track == "d_runni2") track = "h_runnin";
            else if (track == "d_shawn" || track == "d_shawn2" || track == "d_shawn3") track = "h_shawn";
            else if (track == "d_stalks" || track == "d_stlks2" || track == "d_stlks3") track = "h_stalks";
            else if (track == "d_tense") track = "h_tense";
            else if (track == "d_the_da" || track == "d_theda2" || track == "d_theda3") track = "h_the_da";
            else if (track == "d_ultima") track = "h_ultima";
            else if (track == "d_dm2ttl") track = "h_dm2ttl";
            else if (track == "d_dm2int") track = "h_dm2int";
            else if (track == "d_read_m") track = "h_read_m";
        }
        else if (threeDoOn)
        {
            if (track == "d_e1m1" || track == "h_e1m1") track = "3_e1m1";
            else if (track == "d_e1m2" || track == "h_e1m2") track = "3_e1m2";
            else if (track == "d_e1m3" || track == "h_e1m3") track = "3_e1m3";
            else if (track == "d_e1m4" || track == "h_e1m4") track = "3_e1m4";
            else if (track == "d_e1m5" || track == "h_e1m5") track = "3_e1m5";
            else if (track == "d_e1m6" || track == "h_e1m6") track = "3_e1m6";
            else if (track == "d_e1m7" || track == "h_e1m7") track = "3_e1m7";
            else if (track == "d_e1m8" || track == "h_e1m8") track = "3_e1m8";
            else if (track == "d_e1m9" || track == "h_e1m9") track = "3_e1m9";
            else if (track == "d_e2m1" || track == "h_e2m1") track = "3_e2m1";
            else if (track == "d_e2m2" || track == "h_e2m2") track = "3_e2m2";
            else if (track == "d_e2m3" || track == "h_e2m3") track = "3_e2m3";
            else if (track == "d_e2m4" || track == "h_e2m4") track = "3_e2m4";
            else if (track == "d_e2m5" || track == "h_e2m5") track = "3_e2m5";
            else if (track == "d_e2m6" || track == "h_e2m6") track = "3_e2m6";
            else if (track == "d_e2m7" || track == "h_e2m7") track = "3_e2m7";
            else if (track == "d_e2m8" || track == "h_e2m8") track = "3_e2m8";
            else if (track == "d_e2m9" || track == "h_e2m9") track = "3_e2m9";
            else if (track == "d_e3m1") track = "3_e3m1";
            else if (track == "d_e3m2" || track == "h_e3m2") track = "3_e3m2";
            else if (track == "d_e3m3" || track == "h_e3m3") track = "3_e3m3";
            else if (track == "d_e3m4") track = "3_e3m4";
            else if (track == "d_e3m5") track = "3_e3m5";
            else if (track == "d_e3m6") track = "3_e3m6";
            else if (track == "d_e3m7") track = "3_e3m7";
            else if (track == "d_e3m8" || track == "h_e3m8") track = "3_e3m8";
            else if (track == "d_e3m9") track = "3_e3m9";
            else if (track == "d_inter") track = "3_inter";
            else if (track == "d_intro" || track == "d_introa" || track == "h_intro") track = "3_intro";
            else if (track == "d_victor" || track == "h_victor") track = "3_victor";
            else if (track == "d_bunny" || track == "h_bunny") track = "3_bunny";
        }
        else
        {
            track = MidiForHulshultOr3DO(track, mapName);
        }

        PlayIfChanged(track);
    }
}