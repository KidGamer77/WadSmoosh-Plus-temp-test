//-----------------------------------------------------------------------------
// WadSmoosh Plus / UZDoom 5.x status bar
// Defines WadFusionStatusBar and alias WadFusionStatusBarId24.
// Never compile wf_sbar.id1.zs in the same build.
//-----------------------------------------------------------------------------

class WadFusionStatusBar : BaseStatusBar
{
    HUDFont mHUDFont;
    HUDFont mIndexFont;
    HUDFont mAmountFont;
    InventoryBarState diparms;

    private int CVInt(Name n, int fallback = 0)
    {
        let cv = CVar.FindCVar(n);
        if (cv == null) return fallback;
        return cv.GetInt();
    }

    private bool CVBool(Name n, bool fallback = false)
    {
        let cv = CVar.FindCVar(n);
        if (cv == null) return fallback;
        return cv.GetBool();
    }

    private bool HasGfx(string name)
    {
        return TexMan.CheckForTexture(name, TexMan.Type_Any).IsValid();
    }

    private bool IsLoRMap()
    {
        string mapName = level.MapName.MakeLower();
        string prefix = mapName.Left(3);
        return (prefix == "lr_" || prefix == "dm_");
    }

    private int WeapSwapMode()
    {
        return CVInt("wf_id1_weapswap", 1);
    }

    private bool UseFuelBar()
    {
        int mode = WeapSwapMode();
        if (mode >= 2) return true;
        return (mode == 1 && IsLoRMap());
    }

    override void Init()
    {
        Super.Init();
        SetSize(32, 320, 200);

        Font fnt = "HUDFONT_DOOM";
        mHUDFont = HUDFont.Create(fnt, fnt.GetCharWidth("0"), Mono_CellLeft, 1, 1);
        fnt = "INDEXFONT_DOOM";
        mIndexFont = HUDFont.Create(fnt, fnt.GetCharWidth("0"), Mono_CellLeft);
        mAmountFont = HUDFont.Create("INDEXFONT");
        diparms = InventoryBarState.Create();
    }

    override void Draw(int state, double TicFrac)
    {
        Super.Draw(state, TicFrac);

        if (CPlayer == null || CPlayer.mo == null)
            return;

        if (state == HUD_StatusBar)
        {
            BeginStatusBar();
            DrawMainBar(TicFrac);
        }
        else if (state == HUD_Fullscreen)
        {
            BeginHUD();
            DrawFullScreenStuff();
        }
    }

    protected void DrawMainBar(double TicFrac)
    {
        if (UseFuelBar() && HasGfx("STBRFUEL"))
            DrawImage("STBRFUEL", (-128, 168), DI_ITEM_OFFSETS);
        else
            DrawImage("STBAR", (0, 168), DI_ITEM_OFFSETS);

        DrawImage("STTPRCNT", (90, 171), DI_ITEM_OFFSETS);
        DrawImage("STTPRCNT", (221, 171), DI_ITEM_OFFSETS);

        Inventory a1 = GetCurrentAmmo();
        if (a1 != null)
            DrawString(mHUDFont, FormatNumber(a1.Amount, 3), (44, 171), DI_TEXT_ALIGN_RIGHT|DI_NOSHADOW);

        DrawString(mHUDFont, FormatNumber(CPlayer.health, 3), (90, 171), DI_TEXT_ALIGN_RIGHT|DI_NOSHADOW);
        DrawString(mHUDFont, FormatNumber(GetArmorAmount(), 3), (221, 171), DI_TEXT_ALIGN_RIGHT|DI_NOSHADOW);

        DrawBarKeys();
        DrawBarAmmo();

        if (deathmatch || teamplay)
            DrawString(mHUDFont, FormatNumber(CPlayer.FragCount, 3), (138, 171), DI_TEXT_ALIGN_RIGHT);
        else
            DrawBarWeapons();

        if (multiplayer)
            DrawImage("STFBANY", (143, 168), DI_ITEM_OFFSETS|DI_TRANSLATABLE);

        if (CPlayer.mo.InvSel != null && !Level.NoInventoryBar)
        {
            DrawInventoryIcon(CPlayer.mo.InvSel, (160, 198), DI_DIMDEPLETED);
            if (CPlayer.mo.InvSel.Amount > 1)
            {
                DrawString(mAmountFont, FormatNumber(CPlayer.mo.InvSel.Amount),
                    (175, 198 - mIndexFont.mFont.GetHeight()), DI_TEXT_ALIGN_RIGHT, Font.CR_GOLD);
            }
        }
        else
        {
            DrawTexture(GetMugShot(5), (143, 168), DI_ITEM_OFFSETS);
        }

        if (isInventoryBarVisible())
            DrawInventoryBar(diparms, (48, 169), 7, DI_ITEM_LEFT_TOP);
    }

    protected virtual void DrawBarKeys()
    {
        bool locks[6];
        String image;
        for (int i = 0; i < 6; i++)
            locks[i] = CPlayer.mo.CheckKeys(i + 1, false, true);

        if (locks[1] && locks[4]) image = "STKEYS6";
        else if (locks[1]) image = "STKEYS0";
        else if (locks[4]) image = "STKEYS3";
        else image = "";
        DrawImage(image, (239, 171), DI_ITEM_OFFSETS);

        if (locks[2] && locks[5]) image = "STKEYS7";
        else if (locks[2]) image = "STKEYS1";
        else if (locks[5]) image = "STKEYS4";
        else image = "";
        DrawImage(image, (239, 181), DI_ITEM_OFFSETS);

        if (locks[0] && locks[3]) image = "STKEYS8";
        else if (locks[0]) image = "STKEYS2";
        else if (locks[3]) image = "STKEYS5";
        else image = "";
        DrawImage(image, (239, 191), DI_ITEM_OFFSETS);
    }

    protected virtual void DrawBarAmmo()
    {
        int amt1, maxamt;
        bool id24hud = CVBool("wf_hud_id24", false) || UseFuelBar();

        if (id24hud && HasGfx("STAMMO24"))
            DrawImage("STAMMO24", (249, 168), DI_ITEM_OFFSETS);

        [amt1, maxamt] = GetAmount("Clip");
        DrawString(mIndexFont, FormatNumber(amt1, 3), (288, 173), DI_TEXT_ALIGN_RIGHT);
        DrawString(mIndexFont, FormatNumber(maxamt, 3), (314, 173), DI_TEXT_ALIGN_RIGHT);

        [amt1, maxamt] = GetAmount("Shell");
        DrawString(mIndexFont, FormatNumber(amt1, 3), (288, 179), DI_TEXT_ALIGN_RIGHT);
        DrawString(mIndexFont, FormatNumber(maxamt, 3), (314, 179), DI_TEXT_ALIGN_RIGHT);

        [amt1, maxamt] = GetAmount("RocketAmmo");
        DrawString(mIndexFont, FormatNumber(amt1, 3), (288, 185), DI_TEXT_ALIGN_RIGHT);
        DrawString(mIndexFont, FormatNumber(maxamt, 3), (314, 185), DI_TEXT_ALIGN_RIGHT);

        if (CPlayer.mo.FindInventory("ID24Fuel") != null)
            [amt1, maxamt] = GetAmount("ID24Fuel");
        else
            [amt1, maxamt] = GetAmount("Cell");

        DrawString(mIndexFont, FormatNumber(amt1, 3), (288, 191), DI_TEXT_ALIGN_RIGHT);
        DrawString(mIndexFont, FormatNumber(maxamt, 3), (314, 191), DI_TEXT_ALIGN_RIGHT);
    }

    protected virtual void DrawBarWeapons()
    {
        DrawImage("STARMS", (104, 168), DI_ITEM_OFFSETS);
        DrawImage(CPlayer.HasWeaponsInSlot(2) ? "STYSNUM2" : "STGNUM2", (111, 172), DI_ITEM_OFFSETS);
        DrawImage(CPlayer.HasWeaponsInSlot(3) ? "STYSNUM3" : "STGNUM3", (123, 172), DI_ITEM_OFFSETS);
        DrawImage(CPlayer.HasWeaponsInSlot(4) ? "STYSNUM4" : "STGNUM4", (135, 172), DI_ITEM_OFFSETS);
        DrawImage(CPlayer.HasWeaponsInSlot(5) ? "STYSNUM5" : "STGNUM5", (111, 182), DI_ITEM_OFFSETS);
        DrawImage(CPlayer.HasWeaponsInSlot(6) ? "STYSNUM6" : "STGNUM6", (123, 182), DI_ITEM_OFFSETS);
        DrawImage(CPlayer.HasWeaponsInSlot(7) ? "STYSNUM7" : "STGNUM7", (135, 182), DI_ITEM_OFFSETS);
    }

    protected void DrawFullScreenStuff()
    {
        int ultraWide = CVInt("wf_hud_ultrawide", 0);
        bool swapHA = CVBool("wf_hud_swaphealtharmor", false);

        let berserk = CPlayer.mo.FindInventory("PowerStrength");
        Vector2 healthPos = swapHA ? (20 + ultraWide, -22) : (20 + ultraWide, -2);
        Vector2 armorPos  = swapHA ? (20 + ultraWide, -2)  : (20 + ultraWide, -22);

        DrawImage((berserk != null) ? "PSTRA0" : "MEDIA0", healthPos);
        DrawString(mHUDFont, FormatNumber(CPlayer.health, 3),
            (40 + ultraWide, healthPos.Y - 16), DI_TEXT_ALIGN_LEFT|DI_NOSHADOW);

        let armor = CPlayer.mo.FindInventory("BasicArmor");
        if (armor != null && armor.Amount > 0)
        {
            DrawInventoryIcon(armor, armorPos);
            DrawString(mHUDFont, FormatNumber(armor.Amount, 3),
                (40 + ultraWide, armorPos.Y - 16), DI_TEXT_ALIGN_LEFT|DI_NOSHADOW);
        }

        Inventory ammo = GetCurrentAmmo();
        if (ammo != null)
        {
            DrawInventoryIcon(ammo, (-14 - ultraWide, -4));
            DrawString(mHUDFont, FormatNumber(ammo.Amount, 3),
                (-30 - ultraWide, -20), DI_TEXT_ALIGN_RIGHT|DI_NOSHADOW);
        }

        if (deathmatch || teamplay)
        {
            DrawString(mHUDFont, FormatNumber(CPlayer.FragCount, 3),
                (0, -16), DI_TEXT_ALIGN_CENTER|DI_NOSHADOW);
        }

        DrawFullscreenKeys(ultraWide);

        if (CPlayer.mo.InvSel != null && !Level.NoInventoryBar)
        {
            DrawInventoryIcon(CPlayer.mo.InvSel, (0, -40), DI_DIMDEPLETED);
            if (CPlayer.mo.InvSel.Amount > 1)
            {
                DrawString(mAmountFont, FormatNumber(CPlayer.mo.InvSel.Amount),
                    (8, -40), DI_TEXT_ALIGN_LEFT, Font.CR_GOLD);
            }
        }

        if (isInventoryBarVisible())
            DrawInventoryBar(diparms, (0, -40), 7, DI_SCREEN_CENTER_BOTTOM, HX_SHADOW);
    }

    protected void DrawFullscreenKeys(int ultraWide)
    {
        bool locks[6];
        for (int i = 0; i < 6; i++)
            locks[i] = CPlayer.mo.CheckKeys(i + 1, false, true);

        double x = -18 - ultraWide;
        double y = -40;
        if (locks[1]) DrawImage("STKEYS0", (x, y), DI_ITEM_OFFSETS);
        if (locks[4]) DrawImage("STKEYS3", (x + 10, y), DI_ITEM_OFFSETS);
        if (locks[2]) DrawImage("STKEYS1", (x, y + 10), DI_ITEM_OFFSETS);
        if (locks[5]) DrawImage("STKEYS4", (x + 10, y + 10), DI_ITEM_OFFSETS);
        if (locks[0]) DrawImage("STKEYS2", (x, y + 20), DI_ITEM_OFFSETS);
        if (locks[3]) DrawImage("STKEYS5", (x + 10, y + 20), DI_ITEM_OFFSETS);
    }
}

class WadFusionStatusBarId24 : WadFusionStatusBar
{
}