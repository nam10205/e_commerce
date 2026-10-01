import com.vp.plugin.*;
import com.vp.plugin.model.*;
import com.vp.plugin.model.factory.*;
import com.vp.plugin.diagram.*;
import com.vp.plugin.diagram.shape.*;
import java.awt.*;
import java.awt.geom.Point2D;
import java.io.File;
import java.nio.file.Files;

public class ApiReference implements VPPlugin,VPPluginCommandLineSupport {
 private static final Color CYAN=new Color(122,207,244);
 private ApplicationManager app; private DiagramManager dm; private IModelElementFactory f;
 public void loaded(VPPluginInfo info){} public void unloaded(){}
 private IShapeUIModel shape(IDiagramUIModel d,IModelElement m,String n,int x,int y,int w,int h){
  m.setName(n);IShapeUIModel s=(IShapeUIModel)dm.createDiagramElement(d,m);s.setBounds(x,y,w,h);s.getElementFont().setName("Arial");s.getElementFont().setSize(12);s.resetCaption();s.setBackground(CYAN);s.getFillColor().setValues(1,CYAN,CYAN,0,0,false);return s;
 }
 private IConnectorUIModel connector(IDiagramUIModel d,IModelElement relation,IShapeUIModel from,IShapeUIModel to,Point[] points){
  IConnectorUIModel c=(IConnectorUIModel)dm.createConnector(d,relation,from,to,points);c.getElementFont().setSize(11);c.resetCaption();return c;
 }
 private void include(IDiagramUIModel d,IUseCase[] u,IShapeUIModel[] s,int from,int to,Point[] points){IInclude r=f.createInclude();r.setFrom(u[from]);r.setTo(u[to]);connector(d,r,s[from],s[to],points);}
 private void extend(IDiagramUIModel d,IUseCase[] u,IShapeUIModel[] s,int from,int to,Point[] points){
  IExtend r=f.createExtend();r.setFrom(u[to]);r.setTo(u[from]);IExtensionPoint ep=f.createExtensionPoint();ep.setName("after results are shown");u[to].addChild(ep);r.setExtensionPoint(ep);r.setCondition("Customer chooses to view details");
  if(points!=null){Point[] reversed=new Point[points.length];for(int i=0;i<points.length;i++)reversed[i]=points[points.length-1-i];points=reversed;}connector(d,r,s[to],s[from],points);
 }
 private void build(){
  IProject project=app.getProjectManager().getProject();
  for(IDiagramUIModel old:project.toDiagramArray())if(old.getType().equals("UseCaseDiagram")){
   IDiagramElement[] e=old.toDiagramElementArray();for(IDiagramElement a:e)if(a instanceof IConnectorUIModel)a.getModelElement().delete();for(IDiagramElement a:e)if(a.getModelElement() instanceof IUseCase)a.getModelElement().delete();for(IDiagramElement a:e)if(a.getModelElement() instanceof IActor||a.getModelElement() instanceof ISystem)a.getModelElement().delete();old.delete();
  }
  IDiagramUIModel d=dm.createDiagram(DiagramManager.DIAGRAM_TYPE_USE_CASE_DIAGRAM);d.setName("01 - Use Case Model");
  IActor actor=f.createActor();IShapeUIModel a=shape(d,actor,"Customer",35,220,40,75);
  ISystem system=f.createSystem();ISystemUIModel boundary=(ISystemUIModel)shape(d,system,"Multimodal E-Commerce Search System",140,20,660,600);
  String[] names={"Search Product","Search by Keyword","Search by Image","Search by Voice","View Product","Search Order","View Order","Create Image Vector","Transcribe Speech","Display Search Results","Rank Search Results","Validate Input"};
  int[][] b={{175,170,170,80},{425,45,130,50},{425,115,130,50},{425,190,130,50},{195,500,130,50},{425,545,135,50},{645,545,135,50},{635,115,150,50},{635,190,150,50},{425,275,155,50},{425,355,155,50},{425,435,155,50}};
  IUseCase[] u=new IUseCase[12];IShapeUIModel[] s=new IShapeUIModel[12];for(int i=0;i<12;i++){u[i]=f.createUseCase();system.addChild(u[i]);s[i]=shape(d,u[i],names[i],b[i][0],b[i][1],b[i][2],b[i][3]);((IUseCaseUIModel)s[i]).setShowExtensionPoint(false);boundary.addChild(s[i]);}
  IGeneralization g=f.createGeneralization();g.setFrom(u[0]);g.setTo(u[1]);connector(d,g,s[0],s[1],new Point[]{new Point(235,170),new Point(235,70),new Point(425,70)});
  g=f.createGeneralization();g.setFrom(u[0]);g.setTo(u[2]);connector(d,g,s[0],s[2],new Point[]{new Point(310,170),new Point(310,140),new Point(425,140)});
  g=f.createGeneralization();g.setFrom(u[0]);g.setTo(u[3]);connector(d,g,s[0],s[3],null);
  IAssociation association=f.createAssociation();association.setFrom(actor);association.setTo(u[0]);connector(d,association,a,s[0],new Point[]{new Point(55,220),new Point(55,210),new Point(175,210)});
  association=f.createAssociation();association.setFrom(actor);association.setTo(u[5]);connector(d,association,a,s[5],new Point[]{new Point(55,295),new Point(55,570),new Point(425,570)});
  include(d,u,s,2,7,null);include(d,u,s,3,8,null);
  include(d,u,s,0,9,new Point[]{new Point(310,250),new Point(310,300),new Point(425,300)});
  include(d,u,s,0,10,new Point[]{new Point(280,250),new Point(280,380),new Point(425,380)});
  include(d,u,s,0,11,new Point[]{new Point(250,250),new Point(250,460),new Point(425,460)});
  include(d,u,s,5,11,null);
  extend(d,u,s,4,0,new Point[]{new Point(260,500),new Point(205,500),new Point(205,250)});
  extend(d,u,s,6,5,null);
  for(IShapeUIModel sh:s)((IUseCaseUIModel)sh).setShowExtensionPoint(false);
  for(IDiagramUIModel diagram:project.toDiagramArray())for(IDiagramElement e:diagram.toDiagramElementArray())if(e instanceof IShapeUIModel && !(e.getModelElement() instanceof IFrame)){IShapeUIModel sh=(IShapeUIModel)e;sh.setBackground(CYAN);sh.getFillColor().setValues(1,CYAN,CYAN,0,0,false);}
 }
 public void invoke(String[] args){try{
  app=ApplicationManager.instance();dm=app.getDiagramManager();f=IModelElementFactory.instance();boolean verify=args.length>1&&args[1].equals("verify");if(!verify)build();
  IProject p=app.getProjectManager().getProject();int uc=0,inc=0,ext=0,gen=0,assoc=0;StringBuilder json=new StringBuilder("{\"reopened\":").append(verify).append(",\"diagram_count\":").append(p.toDiagramArray().length).append(",\"diagrams\":[");int index=0;
  for(IDiagramUIModel d:p.toDiagramArray()){if(index++>0)json.append(',');json.append("{\"name\":\"").append(d.getName()).append("\",\"type\":\"").append(d.getType()).append("\",\"elements\":").append(d.toDiagramElementArray().length).append('}');if(d.getType().equals("UseCaseDiagram"))for(IDiagramElement e:d.toDiagramElementArray()){IModelElement m=e.getModelElement();if(m instanceof IUseCase)uc++;if(m instanceof IInclude)inc++;if(m instanceof IExtend)ext++;if(m instanceof IGeneralization)gen++;if(m instanceof IAssociation)assoc++;}}
  if(p.toDiagramArray().length!=3||uc!=12||inc!=6||ext!=2||gen!=3||assoc!=2)throw new IllegalStateException("Unexpected native UML counts: "+uc+","+inc+","+ext+","+gen+","+assoc);
  for(IDiagramUIModel d:p.toDiagramArray()){
   for(IDiagramElement e:d.toDiagramElementArray())if(e instanceof IShapeUIModel && !(e.getModelElement() instanceof IFrame) && !CYAN.equals(e.getBackground()))throw new IllegalStateException("Fill not persisted: "+e.getModelElement().getName());
   if(verify){String stem=d.getType().equals("UseCaseDiagram")?"01_use_case":d.getType().equals("ComponentDiagram")?"02_architecture":"03_voice_sequence";ExportDiagramAsImageOption option=new ExportDiagramAsImageOption(0);option.setScale(2f);option.setTextAntiAliasing(true);option.setGraphicAntiAliasing(true);app.getModelConvertionManager().exportDiagramAsImage(d,new File(args[0],"uml/"+stem+".png"),option);}
  }
  json.append("],\"use_cases\":12,\"include_relationships\":6,\"extend_relationships\":2,\"generalizations\":3,\"associations\":2,\"color\":\"#7ACFF4\"}");
  if(!verify&&!app.getProjectManager().saveProject())throw new IllegalStateException("Save failed");Files.write(new File(args[0],"demo/uml_verification.json").toPath(),json.toString().getBytes("UTF-8"));
  System.out.println("REFERENCE_UML_SUCCESS="+json);
 }catch(Exception e){throw new RuntimeException(e);}}
}
