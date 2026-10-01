import com.vp.plugin.*;
import com.vp.plugin.model.*;
import com.vp.plugin.model.factory.*;
import com.vp.plugin.diagram.*;
import com.vp.plugin.diagram.shape.*;
import com.vp.plugin.diagram.connector.*;
import java.awt.*;
import java.io.*;
public class ApiBuilder implements VPPlugin, VPPluginCommandLineSupport {
 private ApplicationManager app; private DiagramManager dm; private IModelElementFactory f; private File output;
 public void loaded(VPPluginInfo info){System.out.println("BUILDER LOADED");}
 public void unloaded(){}
 private IDiagramElement shape(IDiagramUIModel d,IModelElement m,String name,int x,int y,int w,int h){
   m.setName(name);IDiagramElement s=dm.createDiagramElement(d,m);s.setBounds(x,y,w,h);
   s.getElementFont().setSize(15);s.getElementFont().setName("Arial");s.resetCaption();if(s instanceof IShapeUIModel){Color fill=(m instanceof ISystem)?Color.WHITE:new Color(194,222,255);s.setBackground(fill);((IShapeUIModel)s).getFillColor().setColor1(fill,false);}return s;
 }
 private void dep(IDiagramUIModel d,IDiagramElement a,IDiagramElement b,Point[] pts){
   IDependency rel=f.createDependency();rel.setFrom(a.getModelElement());rel.setTo(b.getModelElement());dm.createConnector(d,rel,a,b,pts);
 }
 private void useCaseConnector(IConnectorUIModel c,boolean actor){
   c.setConnectorStyle(IConnectorUIModel.CS_OBLIQUE);c.setFromPinType(IConnectorUIModel.PINTYPE_RATIO);c.setToPinType(IConnectorUIModel.PINTYPE_RATIO);
   c.setFromPinRatio(new java.awt.geom.Point2D.Double(actor?0.5:1.0,actor?0.45:0.5));c.setToPinRatio(new java.awt.geom.Point2D.Double(0,0.5));
   c.clearPoints();c.setRequestRebuild(true);c.setRequestRebuildFromEnd(true);c.setRequestRebuildToEnd(true);
 }
 private void export(IDiagramUIModel d,String stem)throws Exception{
   ExportDiagramAsImageOption o=new ExportDiagramAsImageOption(0);o.setScale(2f);o.setTextAntiAliasing(true);o.setGraphicAntiAliasing(true);
   app.getModelConvertionManager().exportDiagramAsImage(d,new File(output,"uml/"+stem+".png"),o);
 }
 private void usecases()throws Exception {
   IDiagramUIModel d=dm.createDiagram(DiagramManager.DIAGRAM_TYPE_USE_CASE_DIAGRAM);d.setName("01 - Use Case Model");
   IActor actor=f.createActor();IDiagramElement a=shape(d,actor,"Customer",35,275,40,80);a.getElementFont().setSize(12);a.resetCaption();
   ISystem sys=f.createSystem();ISystemUIModel boundary=(ISystemUIModel)shape(d,sys,"Multimodal E-Commerce Search System",165,30,645,520);boundary.getElementFont().setSize(12);boundary.resetCaption();
   String[] names={"Search Product","Search by Keyword","Search by Voice","Search by Image","Search Order","View Product","View Order"};
   int[][] xy={{240,130},{590,65},{590,145},{590,225},{240,375},{240,285},{240,465}};
   IDiagramElement[] s=new IDiagramElement[7];IUseCase[] uc=new IUseCase[7];
   for(int i=0;i<7;i++){uc[i]=f.createUseCase();sys.addChild(uc[i]);s[i]=shape(d,uc[i],names[i],xy[i][0],xy[i][1],(i>=1&&i<=3)?175:160,(i>=1&&i<=3)?50:55);s[i].getElementFont().setSize(12);s[i].resetCaption();boundary.addChild((IShapeUIModel)s[i]);}
   for(int i=1;i<=3;i++){IGeneralization r=f.createGeneralization();r.setFrom(uc[0]);r.setTo(uc[i]);useCaseConnector((IConnectorUIModel)dm.createConnector(d,r,s[0],s[i],null),false);}
   for(int i:new int[]{0,4,5,6}){IAssociation r=f.createAssociation();r.setFrom(actor);r.setTo(uc[i]);useCaseConnector((IConnectorUIModel)dm.createConnector(d,r,a,s[i],null),true);}
   export(d,"01_use_case");
 }
 private void architecture()throws Exception {
   IDiagramUIModel d=dm.createDiagram(DiagramManager.DIAGRAM_TYPE_COMPONENT_DIAGRAM);d.setName("02 - Three-Layer Components");
   String[] layers={"Presentation Layer","Application / Intelligence Layer","Data Layer"};
   int[] ys={40,330,650};IDiagramElement[] packs=new IDiagramElement[3];IPackage[] pm=new IPackage[3];
   for(int i=0;i<3;i++){pm[i]=f.createPackage();packs[i]=shape(d,pm[i],layers[i],40,ys[i],900,i==0?220:250);packs[i].setBackground(new Color(235,244,255));((IShapeUIModel)packs[i]).getFillColor().setColor1(new Color(235,244,255),false);}
   String[][] names={{"SearchUI","VoiceInput","ImageUpload","SearchResultView"},{"QueryService","SpeechService","ImageService","SearchService","RankingService"},{"ProductRepository","OrderRepository","VectorIndex","ProductDatabase","OrderDatabase","ImageStorage"}};
   int[][][] coords={{{390,95},{100,185},{680,185},{390,185}},{{110,380},{110,480},{680,480},{390,380},{680,380}},{{110,700},{390,700},{680,700},{110,820},{390,820},{680,820}}};
   IDiagramElement[][] s=new IDiagramElement[3][];
   for(int k=0;k<3;k++){s[k]=new IDiagramElement[names[k].length];for(int j=0;j<names[k].length;j++){IComponent c=f.createComponent();pm[k].addChild(c);s[k][j]=shape(d,c,names[k][j],coords[k][j][0],coords[k][j][1],200,55);packs[k].addChild((IShapeUIModel)s[k][j]);}}
   dep(d,s[0][0],s[1][3],new Point[]{new Point(490,150),new Point(640,150),new Point(640,295),new Point(490,295),new Point(490,380)});
   dep(d,s[0][0],s[1][0],new Point[]{new Point(390,120),new Point(350,120),new Point(350,302),new Point(210,302),new Point(210,380)});
   dep(d,s[1][3],s[1][0],null);dep(d,s[1][3],s[1][4],null);
   dep(d,s[0][1],s[1][1],new Point[]{new Point(200,240),new Point(65,240),new Point(65,507),new Point(110,507)});
   dep(d,s[0][2],s[1][2],new Point[]{new Point(780,240),new Point(990,240),new Point(990,507),new Point(880,507)});
   dep(d,s[1][3],s[2][1],new Point[]{new Point(490,435),new Point(490,700)});
   dep(d,s[1][3],s[2][0],new Point[]{new Point(435,435),new Point(435,610),new Point(210,610),new Point(210,700)});
   dep(d,s[1][3],s[2][2],new Point[]{new Point(545,435),new Point(545,610),new Point(780,610),new Point(780,700)});
   dep(d,s[2][0],s[2][3],null);dep(d,s[2][1],s[2][4],null);
   dep(d,s[1][2],s[2][5],new Point[]{new Point(880,507),new Point(930,507),new Point(930,847),new Point(880,847)});
   export(d,"02_architecture");
 }
 private void sequence()throws Exception {
   IInteractionDiagramUIModel d=(IInteractionDiagramUIModel)dm.createDiagram(DiagramManager.DIAGRAM_TYPE_INTERACTION_DIAGRAM);d.setName("03 - Voice Search Sequence");IFrame root=d.getRootFrame(true);
   String[] names={"Customer","SearchUI","SpeechService","QueryService","SearchService","ProductRepository","RankingService"};
   IInteractionLifeLine[] ll=new IInteractionLifeLine[7];IInteractionLifeLineUIModel[] s=new IInteractionLifeLineUIModel[7];IActivation[] act=new IActivation[7];
   for(int i=0;i<7;i++){IClass c=f.createClass();c.setName(names[i]);ll[i]=f.createInteractionLifeLine();root.addChild(ll[i]);ll[i].setBaseClassifier(c);ll[i].setName("");s[i]=(IInteractionLifeLineUIModel)shape(d,ll[i],"",30+i*200,35,175,950);s[i].resetCaption();
    act[i]=f.createActivation();ll[i].addActivation(act[i]);if(i>0){int[] starts={0,135,210,340,470,535,665};int[] heights={0,740,75,75,335,75,75};IActivationUIModel ac=(IActivationUIModel)dm.createDiagramElement(d,act[i]);ac.setBounds(111+i*200,starts[i],12,heights[i]);ac.setBackground(new Color(194,222,255));ac.getFillColor().setColor1(new Color(194,222,255),false);}}
   int[][] ends={{0,1},{1,2},{2,1},{1,3},{3,1},{1,4},{4,5},{5,4},{4,6},{6,4},{4,1},{1,0}};
   String[] labels={"voice input (transcript)","transcribe(audio_input)","text","voice_query(text)","CommonQuery(type=voice)","search(query, top_k=5)","all_products()","12 products / metadata","rank(candidates, query)","ranked top-k","SearchResult[]","display ranked products"};
   for(int i=0;i<ends.length;i++){int from=ends[i][0],to=ends[i][1],y=145+i*65;IMessage m=f.createMessage();m.setName(labels[i]);m.setSequenceNumber(Integer.toString(i+1));m.setFromActivation(act[from]);m.setToActivation(act[to]);root.addChild(m);
    if(i==2||i==4||i==7||i==9||i==10)m.setActionType(f.createActionTypeReturn());
    IMessageUIModel ms=(IMessageUIModel)dm.createConnector(d,m,s[from],s[to],new Point[]{new Point(117+from*200,y),new Point(117+to*200,y)});ms.getElementFont().setSize(16);ms.resetCaption();}
   export(d,"03_voice_sequence");
 }
 public void invoke(String[] args){try{
   app=ApplicationManager.instance();dm=app.getDiagramManager();f=IModelElementFactory.instance();output=new File(args[0]);new File(output,"uml").mkdirs();
   IProject p=app.getProjectManager().getProject();for(IDiagramUIModel d:p.toDiagramArray())d.delete();for(IModelElement m:p.toModelElementArray()){try{m.delete();}catch(UnsupportedOperationException ignored){}}
   usecases();architecture();sequence();File target=new File(output,"uml/assignment06_multimodal_search.vpp");
   boolean ok=app.getProjectManager().saveProjectAs(target);System.out.println("ASSIGNMENT_SAVE="+ok+" DIAGRAMS="+p.toDiagramArray().length);if(!ok)throw new RuntimeException("Save failed");

 }catch(Throwable e){e.printStackTrace();throw new RuntimeException(e);}}
}



