class WadFusionHandler : EventHandler
{
    private bool CVBoolAlias(string primary, string fallback)
    {
        let cv = CVar.FindCVar(primary);
        if (cv != null) return cv.GetBool();
        cv = CVar.FindCVar(fallback);
        return cv != null && cv.GetBool();
    }

    private bool HasTex(string name)
    {
        return TexMan.CheckForTexture(name, TexMan.Type_Any).IsValid();
    }

    private void SwapWall(string from, string to)
    {
        if (HasTex(to))
            Level.ReplaceTextures(from, to, TexMan.NOT_FLAT);
    }

    private void SwapFlat(string from, string to)
    {
        if (HasTex(to))
            Level.ReplaceTextures(from, to, TexMan.NOT_WALL);
    }

    private bool IsMapPrefix(string prefix)
    {
        return Level.MapName.Left(prefix.Length()) ~== prefix;
    }

    private bool IsDoom1StyleMap()
    {
        string m = Level.MapName;
        if (m.Left(1) ~== "E" && m.IndexOf("M") >= 2) return true;
        if (IsMapPrefix("LR_") || IsMapPrefix("JPTR_") || IsMapPrefix("FD1_") || IsMapPrefix("NS_"))
            return true;
        return false;
    }

    private class<Actor> FindActorClass(Name n)
    {
        class<Actor> cls = n;
        return cls;
    }

    private void DoDoom1TextureReplacements()
    {
        if (!CVBoolAlias("wf_d1_texswap", "ws_d1pois_texswap")) return;
        if (!IsDoom1StyleMap()) return;

        SwapWall("BRNPOIS",  "BRNPOIS1");
        SwapWall("NUKEPOIS", "NUKPOIS1");
        SwapWall("BIGDOOR7", "BIGDOR7A");
        SwapWall("SHAWN1",   "SHAWN1A");
        SwapWall("STEP1",    "STEP1A");
        SwapWall("STEP2",    "STEP2A");
        SwapWall("STEP3",    "STEP3A");
        SwapWall("STEP5",    "STEP5A");
        SwapWall("SW1BRN1",  "SW1BRN1A");
        SwapWall("SW1STARG", "SW1STARA");
        SwapWall("SW1STONE", "SW1STONA");
        SwapWall("SW1STON2", "SW1STONB");
        SwapWall("SW2BRN1",  "SW2BRN1A");
        SwapWall("SW2STARG", "SW2STARA");
        SwapWall("SW2STONE", "SW2STONA");
        SwapWall("SW2STON2", "SW2STONB");
    }

    private void DoId1TextureReplacements()
    {
        if (!CVBoolAlias("wf_id1_texswap", "ws_id1_texswap")) return;
        if (!IsMapPrefix("LR_") && !IsMapPrefix("DM_")) return;

        SwapWall("WFALL1", "XWFALL1");
        SwapWall("WFALL2", "XWFALL2");
        SwapWall("WFALL3", "XWFALL3");
        SwapWall("WFALL4", "XWFALL4");
    }

    private void DoTNTTextureReplacements()
    {
        if (!CVBoolAlias("wf_finaldoom_texswap", "ws_finaldoom_texswap")) return;
        if (!(IsMapPrefix("TN_") || IsMapPrefix("T2_") || IsMapPrefix("TR_"))) return;

        SwapWall("BLODGR1",  "BLODGRT1");
        SwapWall("BLODGR4",  "BLODGRT4");
        SwapWall("SLADRIP1", "SLADRPT1");
        SwapWall("SLADRIP3", "SLADRPT3");
        SwapWall("SW1GSTON", "SW1GSTNT");
        SwapWall("SW2GSTON", "SW2GSTNT");
        SwapWall("SW1SKULL", "SW1SKULT");
        SwapWall("SW2SKULL", "SW2SKULT");
        SwapWall("WFALL1",   "TWFALL1");
        SwapWall("WFALL2",   "TWFALL2");
        SwapWall("WFALL3",   "TWFALL3");
        SwapWall("WFALL4",   "TWFALL4");

        if (CVBoolAlias("wf_d2sky_compat", "ws_d2sky_compat"))
        {
            string sky = TexMan.GetName(Level.SkyTexture1);
            if (sky == "SKY1" && HasTex("TSKY1"))
                Level.ChangeSky(TexMan.CheckForTexture("TSKY1"), Level.SkyTexture2);
            else if (sky == "SKY2" && HasTex("TSKY2"))
                Level.ChangeSky(TexMan.CheckForTexture("TSKY2"), Level.SkyTexture2);
            else if (sky == "SKY3" && HasTex("TSKY3"))
                Level.ChangeSky(TexMan.CheckForTexture("TSKY3"), Level.SkyTexture2);
        }
    }

    private void DoPlutoniaTextureReplacements()
    {
        if (!CVBoolAlias("wf_finaldoom_texswap", "ws_finaldoom_texswap")) return;

        string p3 = Level.MapName.Left(3).MakeLower();
        string p4 = Level.MapName.Left(4).MakeUpper();
        if (!(p3 == "pl_" || p3 == "p2_" || p4 == "PRCP")) return;

        SwapWall("FIREBLU1", "FIREPLU1");
        SwapWall("FIREBLU2", "FIREPLU2");
        SwapWall("DBRAIN1",  "PBRAIN1");
        SwapWall("DBRAIN4",  "PBRAIN4");
        SwapWall("SW1SKULL", "SW1SKULP");
        SwapWall("SW2SKULL", "SW2SKULP");
        SwapWall("WFALL1",   "PWFALL1");
        SwapWall("WFALL2",   "PWFALL2");
        SwapWall("WFALL3",   "PWFALL3");
        SwapWall("WFALL4",   "PWFALL4");
        SwapWall("SLIME4",   "PSLIME4");
        SwapFlat("SLIME4",   "SLIME04");

        if (CVBoolAlias("wf_d2sky_compat", "ws_d2sky_compat"))
        {
            string sky = TexMan.GetName(Level.SkyTexture1);
            if (sky == "SKY1" && HasTex("PSKY1"))
                Level.ChangeSky(TexMan.CheckForTexture("PSKY1"), Level.SkyTexture2);
            else if (sky == "SKY2" && HasTex("PSKY2"))
                Level.ChangeSky(TexMan.CheckForTexture("PSKY2"), Level.SkyTexture2);
            else if (sky == "SKY3" && HasTex("PSKY3"))
                Level.ChangeSky(TexMan.CheckForTexture("PSKY3"), Level.SkyTexture2);
        }
    }

    private void DoHell2PayTextureReplacements()
    {
        if (!IsMapPrefix("HP_")) return;
        SwapFlat("NUKAGE1", "HPNUKE1");
        SwapFlat("NUKAGE2", "HPNUKE2");
        SwapFlat("NUKAGE3", "HPNUKE3");
        SwapFlat("FWATER1", "HPFWAT1");
        SwapFlat("FWATER2", "HPFWAT2");
        SwapFlat("FWATER3", "HPFWAT3");
        SwapFlat("FWATER4", "HPFWAT4");
        SwapFlat("BLOOD1",  "HPBLOOD1");
        SwapFlat("BLOOD2",  "HPBLOOD2");
        SwapFlat("BLOOD3",  "HPBLOOD3");
        // HtP serial crates only if those defs exist
        SwapWall("CRATE1",   "HP_CRATE1");
        SwapWall("CRATE2",   "HP_CRATE2");
        SwapWall("CRATE3",   "HP_CRATE3");
        SwapWall("CRATELIT", "HP_CRATELIT");
        SwapWall("CRATINY",  "HP_CRATINY");
        SwapWall("CRATWIDE", "HP_CRATWIDE");
    }

    private void DoDoomZeroFlatReplacements()
    {
        if (!IsMapPrefix("DZ_")) return;
        SwapFlat("FWATER1", "DZFWAT1");
        SwapFlat("FWATER2", "DZFWAT2");
        SwapFlat("FWATER3", "DZFWAT3");
        SwapFlat("FWATER4", "DZFWAT4");
        SwapFlat("SLIME05", "DZSLM05");
        SwapFlat("SLIME06", "DZSLM06");
        SwapFlat("SLIME07", "DZSLM07");
        SwapFlat("SLIME08", "DZSLM08");
        SwapFlat("SLIME09", "DZSLM09");
        SwapFlat("SLIME10", "DZSLM10");
        SwapFlat("SLIME11", "DZSLM11");
        SwapFlat("SLIME12", "DZSLM12");
    }

    private void DoMasterLevelsTextureReplacements()
    {
        if (!CVBoolAlias("wf_masterlevels_texswap", "ws_masterlevels_texswap")) return;
        if (!IsMapPrefix("ML_")) return;

        string m = Level.MapName.MakeLower();
        if ((m == "ml_map05" || m == "ml_map09") && HasTex("ML_SKY1"))
            Level.ChangeSky(TexMan.CheckForTexture("ML_SKY1"), Level.SkyTexture2);
        else if (m == "ml_map16" && HasTex("ML_SKY2"))
            Level.ChangeSky(TexMan.CheckForTexture("ML_SKY2"), Level.SkyTexture2);
        else if ((m == "ml_map11" || m == "ml_map12" || m == "ml_map13"
               || m == "ml_map14" || m == "ml_map15") && HasTex("ML_SKY3"))
            Level.ChangeSky(TexMan.CheckForTexture("ML_SKY3"), Level.SkyTexture2);
    }

    private void DoPerditionSky()
    {
        if (!IsMapPrefix("PG_")) return;

        int n = 0;
        string mapName = Level.MapName.MakeUpper();
        if (mapName.Length() >= 8)
            n = mapName.Mid(6, 2).ToInt();

        string sky;
        if (n >= 21)
            sky = "PG_SKY3";
        else if (n >= 12)
            sky = "PG_SKY2";
        else
            sky = "PG_SKY1";

        if (!HasTex(sky)) return;
        let tex = TexMan.CheckForTexture(sky, TexMan.Type_Any);
        Level.ChangeSky(tex, tex);
    }

    private void DoPerditionCrates()
    {
        if (!IsMapPrefix("PG_")) return;
        SwapWall("CRATE1",   "PGCRATE1");
        SwapWall("CRATE2",   "PGCRATE2");
        SwapWall("CRATE3",   "PGCRATE3");
        SwapWall("CRATELIT", "PGCRATLT");
        SwapWall("CRATINY",  "PGCRATIN");
        SwapWall("CRATWIDE", "PGCRATWD");
    }

    private void RevertKillCounter(Actor mo)
    {
        if (mo == null) return;
        if (!(mo.bIsMonster && mo.bCountKill)) return;
        mo.bCountKill = false;
        Level.Total_Monsters = Max(0, Level.Total_Monsters - 1);
    }

    override void WorldLoaded(WorldEvent e)
    {
        DoDoom1TextureReplacements();
        DoId1TextureReplacements();
        DoTNTTextureReplacements();
        DoPlutoniaTextureReplacements();
        DoHell2PayTextureReplacements();
        DoDoomZeroFlatReplacements();
        DoMasterLevelsTextureReplacements();
        DoPerditionSky();
        DoPerditionCrates();
    }

    override void WorldThingSpawned(WorldEvent e)
    {
        if (e.Thing == null) return;
        if (!CVBoolAlias("wf_killcountfix", "ws_killcountfix")) return;

        string cls = e.Thing.GetClassName();
        if (cls ~== "ID24Ghoul" || cls ~== "ID24Banshee")
        {
            RevertKillCounter(e.Thing);
            return;
        }

        if (Level.MapTime > 0)
            RevertKillCounter(e.Thing);
    }

    override void WorldThingRevived(WorldEvent e)
    {
        if (e.Thing == null) return;
        if (CVBoolAlias("wf_killcountfix", "ws_killcountfix"))
            RevertKillCounter(e.Thing);
    }

    override void CheckReplacement(ReplaceEvent e)
    {
        if (e.Replacee == null) return;

        string mapName = Level.MapName.MakeLower();

        if (CVBoolAlias("wf_sigil2_spiderboss", "ws_sigil2_spiderboss"))
        {
            if (mapName == "e6m8" && e.Replacee == "SpiderMastermind")
            {
                class<Actor> buffed = FindActorClass("SpiderMastermindSigil2");
                if (buffed)
                    e.Replacement = buffed;
            }
        }

        if (mapName == "tr_map30")
        {
            class<Actor> cls;
            if (e.Replacee == "BossBrain")
            {
                cls = FindActorClass("TNTRBossBrain");
                if (cls) e.Replacement = cls;
            }
            else if (e.Replacee == "BossEye")
            {
                cls = FindActorClass("TNTRBossEye");
                if (cls) e.Replacement = cls;
            }
            else if (e.Replacee == "BossTarget")
            {
                cls = FindActorClass("TNTRBossTarget");
                if (cls) e.Replacement = cls;
            }
            else if (e.Replacee == "SpawnShot")
            {
                cls = FindActorClass("TNTRSpawnShot");
                if (cls) e.Replacement = cls;
            }
        }
    }

    override void WorldTick()
    {
        if (Level.MapTime != 1) return;

        string m = Level.MapName.MakeLower();
        if (CVBoolAlias("wf_blackroomswap_e1m4b", "ws_blackroomswap_e1m4b"))
        {
            if (m == "e1m3") Level.NextMap = "E1M4B";
            if (m == "e1m4b") Level.NextMap = "E1M5";
        }
        if (CVBoolAlias("wf_blackroomswap_e1m8b", "ws_blackroomswap_e1m8b"))
        {
            if (m == "e1m7") Level.NextMap = "E1M8B";
            if (m == "e1m8b") Level.NextMap = "E2M1";
        }
    }
}

class SpiderMastermindSigil2 : SpiderMastermind
{
    Default
    {
        Tag "Sigil II Spider Mastermind";
        Health 9000;
        PainChance 20;
        Speed 14;
        Mass 1200;
        +BOSS
        +BOSSDEATH
        +NORADIUSDMG
        +DONTMORPH
        +MISSILEMORE
        +MISSILEEVENMORE
        +NOICEDEATH
    }
}