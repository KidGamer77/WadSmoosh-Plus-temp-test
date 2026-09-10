// res/zscript/wf_pl2boss.zs
// Plutonia 2 MAP30 Gatewatcher face isolation.
// Register this handler in MAPINFO GameInfo AddEventHandlers
// next to "WadFusionHandler":
//   AddEventHandlers = "WadFusionHandler", "WadSmooshPL2Handler"

class WadSmooshPL2Handler : EventHandler
{
    private bool HasTex(String name)
    {
        TextureID t = TexMan.CheckForTexture(name, TexMan.Type_Any);
        return t.IsValid();
    }

    private void SwapWall(String fromName, String toName)
    {
        if (!HasTex(fromName) || !HasTex(toName))
            return;
        Level.ReplaceTextures(fromName, toName, 0);
    }

    private bool IsP2Map()
    {
        return Level.MapName.Left(3).MakeLower() == "p2_";
    }

    private void DoPlutonia2BossFace()
    {
        if (!IsP2Map())
            return;

        SwapWall("ZZZFACE1", "P2FACE1");
        SwapWall("ZZZFACE2", "P2FACE2");
        SwapWall("ZZZFACE3", "P2FACE3");
        SwapWall("ZZZFACE4", "P2FACE4");
        SwapWall("ZZZFACE5", "P2FACE5");
        SwapWall("ZZZFACE6", "P2FACE6");
        SwapWall("ZZZFACE7", "P2FACE7");
        SwapWall("ZZZFACE8", "P2FACE8");
        SwapWall("ZZZFACE9", "P2FACE9");
    }

    override void WorldLoaded(WorldEvent e)
    {
        DoPlutonia2BossFace();
    }
}